"""
build a clients factory for AWS services
"""
from boto3 import Session
from configs.load_env import settings 


class AWSClientFactory:
    
    def _create_session(self) -> Session:
        """
        Create a Boto3 session with the provided credentials and region.
        """
        return Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.region_name,
        )

    def dynamo(self):
        """
        Create a Boto3 DynamoDB client.
        
        :param kwargs: Additional keyword arguments to pass to the client.
        :return: A Boto3 DynamoDB client.
        """
        session = self._create_session()
        return session.client("dynamodb")
    
    def dynamo_table(self, table_name: str):
        """
        Create a Boto3 DynamoDB resource for a specific table.
        
        :param table_name: The name of the DynamoDB table.
        :return: A Boto3 DynamoDB resource for the specified table.
        """
        session = self._create_session()
        return session.resource("dynamodb").Table(table_name)
    
    def s3(self):
        """
        Create a Boto3 S3 client.
        
        :param kwargs: Additional keyword arguments to pass to the client.
        :return: A Boto3 S3 client.
        """
        session = self._create_session()
        return session.client("s3")
    
    def cognito(self):
        """
        Create a Boto3 Cognito client.
        
        :param kwargs: Additional keyword arguments to pass to the client.
        :return: A Boto3 Cognito client.
        """
        session = self._create_session()
        return session.client("cognito-idp")
