import os
import boto3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

region = os.getenv("AWS_REGION", "eu-north-1")
dynamodb = boto3.client('dynamodb', region_name=region)

tables = [
    {
        "TableName": "histock-users",
        "KeySchema": [{"AttributeName": "userId", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "userId", "AttributeType": "S"}],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "histock-sessions",
        "KeySchema": [{"AttributeName": "sessionId", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "sessionId", "AttributeType": "S"}],
        "BillingMode": "PAY_PER_REQUEST"
    },
    {
        "TableName": "histock-messages",
        "KeySchema": [{"AttributeName": "messageId", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "messageId", "AttributeType": "S"},
            {"AttributeName": "sessionId", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "sessionId-index",
                "KeySchema": [{"AttributeName": "sessionId", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ]
    },
    {
        "TableName": "histock-alerts",
        "KeySchema": [{"AttributeName": "alertId", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "alertId", "AttributeType": "S"},
            {"AttributeName": "userId", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "userId-index",
                "KeySchema": [{"AttributeName": "userId", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ]
    },
    {
        "TableName": "histock-user-documents",
        "KeySchema": [{"AttributeName": "docId", "KeyType": "HASH"}],
        "AttributeDefinitions": [
            {"AttributeName": "docId", "AttributeType": "S"},
            {"AttributeName": "userId", "AttributeType": "S"}
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "userId-index",
                "KeySchema": [{"AttributeName": "userId", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"}
            }
        ]
    }
]

existing_tables = dynamodb.list_tables()['TableNames']

for table in tables:
    name = table["TableName"]
    if name in existing_tables:
        print(f"Table {name} already exists. Skipping.")
    else:
        print(f"Creating table {name}...")
        dynamodb.create_table(**table)
        print(f"Table {name} created.")

print("Done checking/creating tables.")
