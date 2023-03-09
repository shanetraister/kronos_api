import requests
from kronos_api.authentication import check_token
import pandas as pd


def get_service_accounts(kronos_credentials, kronos_endpoint, acct_id: str = None):
    # here's where a docstring would go IF I HAD ONE
    # This function will retrive all service accounts or a specific service account
    """Pull a list of service accounts, or a specific service account, from Kronos

    Args:
        kronos_credentials (kronos_credentials): A Kronos credentials object of class kronos_credentials
        kronos_endpoint (kronos_endpoint): A Kronos endpoint object of class kronos_endpoint
        acct_id (str, optional): The account ID of a specific service account. Defaults to None. If present, will return a single service account.

    Returns:
        Pandas DataFrame: A Pandas DataFrame containing the service account information
    """
    check_token(kronos_endpoint, kronos_credentials)
    endpoint = kronos_endpoint.base_url + "v2/companies/|" + kronos_endpoint.company + "/service-accounts"
    
    if acct_id:
        endpoint = endpoint + "/" + acct_id
    
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_endpoint.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/json",
        }

    request = requests.get(endpoint, headers=headers)

    if request.status_code != 200:
        print(f"Status Code: {request.status_code}")
        print(request.content)
        print("Report failed")
    else:
        request_json = request.json()
        if not acct_id:
            print(f"Found {len(request_json['service_accounts'])} reports")
            accounts_df = pd.DataFrame(request_json['service_accounts'])
        else:
            accounts_df = pd.DataFrame.from_dict(request_json, orient='index').T
        return accounts_df

