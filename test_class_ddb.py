
from contextlib import contextmanager

from aws_dynamodb import AWSDynamoDB


@contextmanager
def ddb_table_setup(dynamodb_client):
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

    yield
    table = dynamodb_client.Table("Table")
    table.delete()


@contextmanager
def ddb_table_with_previous_data(dynamodb_client):
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
        with ddb_table_setup(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.table_exist()
            assert expected == True

    def test_table_not_exist(self, dynamodb_client):
        with ddb_table_setup(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("no existing table")
            expected = client.table_exist()
            assert expected == False

    def test_put_item_success(self, dynamodb_client):
        with ddb_table_setup(dynamodb_client):
            data_input = {
                "key": "key_1",
                "sort": "range_1",
                "some_extra_data": "extra_data"
            } 

            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.put_item(data_input)
            assert expected == {"status": "success", "item": data_input}

    def test_put_item_fail(self, dynamodb_client):
        with ddb_table_setup(dynamodb_client):
            data_input = {
                "fail_schema": "no data schema"
            } 

            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.put_item(data_input)
            assert expected ==  {'status': 'error', 'message_error': 'An error occurred (ValidationException) when calling the PutItem operation: One or more parameter values were invalid: Missing the key key in the item'}

    def test_get_item_success_item_found(self, dynamodb_client):
        with ddb_table_with_previous_data(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.get_item({"key": "key", "sort": "sort"})
            assert expected == {'item': {'data': {}, 'key': 'key', 'sort': 'sort'}, 'status': 'success'}

    def test_get_item_success_item_not_found(self, dynamodb_client):
        with ddb_table_with_previous_data(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.get_item({"key": "key", "sort": ""})
            assert expected == {'item': {}, 'status': 'success'}

    def test_get_item_fail(self, dynamodb_client):
        with ddb_table_with_previous_data(dynamodb_client):
            client = AWSDynamoDB()
            client.set_table_name("Table")
            expected = client.get_item({"bad schema": "no value"})
            assert expected == {'status': 'error', 'message_error': 'An error occurred (ValidationException) when calling the GetItem operation: Validation Exception'}
