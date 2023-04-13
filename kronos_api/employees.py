import requests
from kronos_api.authentication import check_token
from io import StringIO
import pandas as pd

# IN PROGRESS
# TODO: Internalize the API and make it more user friendly for this process

def make_new_employee(kronos_endpoint, kronos_credentials, employee: dict):
    """A function to create a new employee in Kronos using the Employee Kronos API

    Args:
        kronos_endpoint (kronos_endpoint): an instance of the `kronos_endpoint` class, containing the API endpoint details.
        kronos_credentials (kronos_credentials): an instance of the `kronos_credentials` class, containing the API key and the current token.
        employee (dict): A dictionary containing the employee details. See the Kronos API documentation for details.
        
    Returns:
        _type_: _description_
    """    
    check_token(kronos_endpoint, kronos_credentials)
    # Here's where we'll assert certain conditions about the employee dictionary
    
    
    
    
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_endpoint.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/json",
        }

    content_length = len(employee)
    # TODO: Change the endpoint url to the employee endpoint
    url = kronos_endpoint.base_url + f"v2/companies/{kronos_endpoint.company}/employees"

    # TODO: Make this a post request to the employees endpoint
    make_employee = requests.post(url, headers=headers, data=employee)
    print(f"Making Employee")
    if make_employee.status_code != 200:
        print(f"Status Code: {make_employee.status_code}")
        print(make_employee.content)
        print("Upload failed")
    else:
        print("Upload successful")
