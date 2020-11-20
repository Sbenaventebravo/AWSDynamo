import boto3
import logging
from decimal import Decimal

from botocore.exceptions import ClientError

from config_loader import get_credentials
from singleton import SingletonMeta


class AWSDynamoDB(metaclass=SingletonMeta):
    def __init__(self, table_name='', env=""):
        self.credentials = get_credentials(env)
        self.session = self.make_session()
        self.dynamodb = self.session.resource(
            'dynamodb',
            region_name=self.credentials["AWS_REGION"]
        )
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)

    def make_session(self) -> boto3.session.Session:
        """ Make boto3 session for the operations, attach aws credentials
            Returns:
                (boto3.session.Session) returns boto3 objet for sessions

        """
        return boto3.session.Session(
            aws_access_key_id=self.credentials["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=self.credentials["AWS_SECRET_ACCESS_KEY"],
            region_name=self.credentials["AWS_REGION"]
        )

    def set_table_name(self, table_name) -> None:
        """ Changes the table conection in the client
            Args:
                table_name     (str): ddb table name

        """
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)

    def table_exist(self) -> bool:
        """ Identify if the current table conection exist.
            Returns:
                (bool) Return True if exist else otherwise

        """
        exist = False
        try:
            exist = self.table.table_status in (
                "CREATING",
                "UPDATING",
                "DELETING",
                "ACTIVE"
            )
        except ClientError:
            logging.error("Table: {} not found".format(self.table_name))

        return exist

    def put_item(self, item) -> dict:
        """ Insert or update an item in the ddb table
            Args:
                item    (dict): table record, you need know
                                 table schema to push data
            Returns:
                (dict) Return a dictionary with the pushed data or error raised

        """
        result = {}
        try:
            item = {
                key: (Decimal(value) if isinstance(value, float) else value)
                for key, value in item.items()
            }
            self.table.put_item(Item=item)
            result["status"] = "success"
            result["item"] = item
        except ClientError as ex:
            logging.error((
                "Error in put item, table_name:{},"
                " data_send:{},"
                " exception_message:{}").format(
                    item,
                    self.table_name,
                    ex
                )
            )
            result["status"] = "error"
            result["message_error"] = str(ex)
        return result

    def get_item(self, primary_key) -> dict:
        """ get an item in the ddb table
            Args:
                primary_key     (dict): table key, you need know
                                 table schema to push data
            Returns:
                (dict) Return a dictionary with the getted data or error raised

        """
        result = {}
        try:
            response = self.table.get_item(
                Key={
                    **primary_key
                }
            )
            item = response.get("Item", {})
            result["status"] = "success"
            result["item"] = item

        except ClientError as ex:
            logging.error((
                "Error in get item, table_name:{},"
                " primary_key_send:{},"
                " exception_message:{}").format(
                    primary_key,
                    self.table_name,
                    ex
                )
            )
            result["status"] = "error"
            result["message_error"] = str(ex)

        return result
