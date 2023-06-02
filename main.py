import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

TENANT_ID = os.getenv('RALLY_TENANT_ID')
APP_ID = os.getenv('PBI_CLIENT_ID')
APP_SECRET = os.getenv('PBI_CLIENT_SECRET')
GROUP_ID = os.getenv('GROUP_ID')
DATASET_ID = os.getenv('DATASET_ID')

AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
RESOURCE_URL = 'https://analysis.windows.net/powerbi/api'
SCOPES = [f'{RESOURCE_URL}/.default']
# API_ENDPOINT = f'https://api.powerbi.com/v1.0/myorg/groups/{GROUP_ID}/datasets/{DATASET_ID}/refreshes'


app = ConfidentialClientApplication(APP_ID, client_credential=APP_SECRET, authority=AUTHORITY)
result = app.acquire_token_for_client(scopes=SCOPES)

if 'access_token' not in result:
    print('No access token')
    exit(1)
access_token = result['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
}

# response = requests.post(url=API_ENDPOINT, headers=headers)
response = requests.get("https://api.powerbi.com/v1.0/myorg/groups/{GROUP_ID}/datasets", headers=headers)
print(f'{response.status_code}\n{response.text}')
