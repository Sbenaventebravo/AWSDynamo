
import boto3
import logging

from botocore.exceptions import ClientError

from singleton import SingletonMeta


class AWSDynamoDB(metaclass=SingletonMeta):
    def __init__(self, table_name='', region_name="us-east-1"):
        self.dynamodb = boto3.resource('dynamodb', region_name)
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)

    def set_table_name(self, table_name) -> None:
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)

    def table_exist(self) -> bool:
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
        result = {}
        try:
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
