
from contextlib import contextmanager

from aws_dynamodb import AWSDynamoDB


@contextmanager
def ddb_table_setup(dynamodb_client):
    """Generate a context mananger who first creates a table
        and finally deletes it
    """
    dynamodb_client.create_table(
            TableName="Table",
            KeySchema=[
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'sort',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'key',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sort',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    table = dynamodb_client.Table("Table")
    yield
    table = dynamodb_client.Table("Table")
    table.delete()


@contextmanager
def ddb_table_with_previous_data(dynamodb_client):
    """Generate a context mananger who first creates a table and a register
        and finally deletes the register and the table
    """
    dynamodb_client.create_table(
            TableName="Table",
            KeySchema=[
                {
                    'AttributeName': 'key',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'sort',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'key',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sort',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    table = dynamodb_client.Table("Table")
    table.put_item(Item={
        "key": "key",
        "sort": "sort",
        "data": {}
    })
    yield

    table.delete_item(
        Key={
            "key": "key",
            "sort": ""
        }
    )
    table.delete()


class TestClassDDB:
    def test_table_exist(self, dynamodb_client):
        """ Verify if the table_exist function can
            validate if the table exist
        """
        with ddb_table_setup(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("Table")
            print(client.dynamodb.meta)
            expected = client.table_exist()
            assert expected is True
