
import os
import boto3

SNS_ENDPOINT_URL = os.getenv(
    "SNS_ENDPOINT_URL",
    "http://localhost:4566",
)

SNS_TOPIC_ARN = os.getenv(
    "SNS_TOPIC_ARN",
    "arn:aws:sns:us-east-1:000000000000:event-announcements",
)

sns_client = boto3.client(
    "sns",
    endpoint_url=SNS_ENDPOINT_URL,
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)


def publish_event_notification(subject, message):
    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject[:100],
        Message=message,
    )
    return response["MessageId"]
