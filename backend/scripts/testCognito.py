import os
import boto3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

client = boto3.client('cognito-idp', region_name=os.getenv("COGNITO_REGION"))

try:
    print("Attempting to sign up dummy user...")
    client.sign_up(
        ClientId=os.getenv("COGNITO_CLIENT_ID"),
        Username="dummytest12345@example.com",
        Password="Password123!",
        UserAttributes=[
            {"Name": "email", "Value": "dummytest12345@example.com"},
            {"Name": "name", "Value": "Dummy"}
        ]
    )
    print("Signup succeeded. Confirming...")
    client.admin_confirm_sign_up(
        UserPoolId=os.getenv("COGNITO_USER_POOL_ID"),
        Username="dummytest12345@example.com"
    )
    
    print("Attempting to log in...")
    response = client.initiate_auth(
        ClientId=os.getenv("COGNITO_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": "dummytest12345@example.com",
            "PASSWORD": "Password123!"
        }
    )
    print("Login successful!")
    print(response)
except Exception as e:
    print("COGNITO ERROR:", e)
