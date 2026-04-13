import json

import boto3
from botocore.exceptions import ClientError


class SecretsManager:
    """Retrieves secrets stored in AWS Secrets Manager."""

    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(service_name="secretsmanager")

    def get_json_creds(self, secret_name: str) -> dict:
        return json.loads(self.get_secret_string(secret_name))

    def get_secret_string(self, secret_name: str) -> str:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]

        except ClientError as e:
            raise ValueError(f"Failed to retrieve secret {secret_name}: {e}")
