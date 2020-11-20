import boto3
import pytest

from moto import mock_dynamodb2


@pytest.yield_fixture(scope="module")
def dynamodb_client():
    """DDB mock client"""
    with mock_dynamodb2():
        session = boto3.session.Session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-2"
        )
        conn = session.resource('dynamodb')

        yield conn
