import os
from unittest.mock import patch
from config_loader import get_credentials


def mock_load_dotenv_prod():
    os.environ["PROD_AWS_ACCESS_KEY_ID"] = "test"
    os.environ["PROD_AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["PROD_AWS_REGION"] = "test"


def mock_load_dotenv_dev():
    os.environ["DEV_AWS_ACCESS_KEY_ID"] = "test"
    os.environ["DEV_AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["DEV_AWS_REGION"] = "test"


def test_get_credentials_production():
    """Testing get_credentials in an production environment"""
    expected = {
        'AWS_ACCESS_KEY_ID': 'test',
        'AWS_SECRET_ACCESS_KEY': 'test',
        'AWS_REGION': 'test'
    }
    with patch('config_loader.load_dotenv', side_effect=mock_load_dotenv_prod):

        result = get_credentials(env="production")

    assert result == expected


def test_get_credentials_default():
    """Testing get_credentials in an development or default environment"""
    expected = {
        'AWS_ACCESS_KEY_ID': 'test',
        'AWS_SECRET_ACCESS_KEY': 'test',
        'AWS_REGION': 'test'
    }
    with patch('config_loader.load_dotenv', side_effect=mock_load_dotenv_dev):

        result = get_credentials()

    assert result == expected
