import os
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

TENANT_ID = os.getenv('TENANT_ID')
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

print(access_token)

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
}


groups = requests.get("https://api.powerbi.com/v1.0/myorg/groups", headers=headers)
# print(f'{groups.status_code}\n{groups.json()}')

for group in groups.json()['value']:
    gid = group.get('id')
    # print(gid, group.get('name'))
    datasets = requests.get(f"https://api.powerbi.com/v1.0/myorg/groups/{gid}/datasets", headers=headers)
    for dataset in datasets.json()['value']:
        # print(f'\t{dataset.get("name")}')
        if dataset.get("name") == 'ARL Balanced Scorecard':
            print(dataset_id := dataset.get("id"))
            refresh = requests.post( f'https://api.powerbi.com/v1.0/myorg/groups/{gid}/datasets/{dataset_id}/refreshes', headers=headers)
            print(refresh.status_code)
            print(refresh.text)
        
    
