import os
from dotenv import load_dotenv


def get_credentials(env="development") -> dict:
    """ Get aws credentials from .env file,
        in this file we define the development and production env
        file structure:
        # Production credentials
        PROD_AWS_ACCESS_KEY_ID =
        PROD_AWS_SECRET_ACCESS_KEY =
        PROD_AWS_REGION =

        # Development credentials
        DEV_AWS_ACCESS_KEY_ID =
        DEV_AWS_SECRET_ACCESS_KEY =
        DEV_AWS_REGION =
        Args:
            env     (str): environment name, development by default

        Returns:
            (dict): dictionary with the respective credetials

    """
    load_dotenv()
    credentials = {}

    credentials["AWS_ACCESS_KEY_ID"] = os.getenv("DEV_AWS_ACCESS_KEY_ID")
    credentials["AWS_SECRET_ACCESS_KEY"] = os.getenv(
        "DEV_AWS_SECRET_ACCESS_KEY")
    credentials["AWS_REGION"] = os.getenv("DEV_AWS_REGION")

    if env == "production":
        credentials["AWS_ACCESS_KEY_ID"] = os.getenv("PROD_AWS_ACCESS_KEY_ID")
        credentials["AWS_SECRET_ACCESS_KEY"] = os.getenv(
            "PROD_AWS_SECRET_ACCESS_KEY")
        credentials["AWS_REGION"] = os.getenv("PROD_AWS_REGION")

    return credentials
