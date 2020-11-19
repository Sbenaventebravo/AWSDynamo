import os
import boto3
import pytest

from moto import mock_dynamodb2

@pytest.fixture(scope='module')
def aws_credentials():
    """ Mock AWS credentials """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

@pytest.yield_fixture(scope="module")
def dynamodb_client(aws_credentials):
    """DDB mock client"""
    with mock_dynamodb2():
        conn = boto3.resource('dynamodb')
        yield conn