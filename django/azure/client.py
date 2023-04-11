import requests
import json
import os
import msal

def get_azure_ad_users():
    # Set up Microsoft Graph API authentication
    config = {
        "authority": "https://login.microsoftonline.com/" + os.environ.get('AZURE_TENANT', default=''),
        "client_id": os.environ.get('AZURE_CLIENT_ID', default=''),
        "client_secret": os.environ.get('AZURE_SECRET', default=''),
        "scope": ["https://graph.microsoft.com/.default"]
    }
    app = msal.ConfidentialClientApplication(
        config["client_id"], authority=config["authority"],
        client_credential=config["client_secret"]
    )
    result = app.acquire_token_silent(config["scope"], account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=config["scope"])
    if "access_token" in result:
        headers = {
            "Authorization": f"Bearer {result['access_token']}",
            "Content-Type": "application/json"
        }

        # Retrieve a list of users from Azure AD using the Microsoft Graph API
        response = requests.get(
            "https://graph.microsoft.com/v1.0/users",
            headers=headers,
        )
        return json.loads(response.text)
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))
        raise ValueError("Could not authenticate with Microsoft Graph API")