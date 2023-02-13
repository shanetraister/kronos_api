import requests
import time

# Let's define a series of error classes to handle different types of errors

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class RefreshError(Exception):
    """Raised when token refresh fails"""
    pass

class MissingCredentialsError(Exception):
    """Raised when credentials are missing"""
    pass

class MissingParameterError(Exception):
    """Raised when a required parameter is missing"""
    pass

# Should we build classes for the objects we're going to be working with?

class kronos_endpoint:
    def __init__(self, base_url: str, api_key: str, username: str, password: str, company: str):
        """Builds a kronos_endpoint object

        Args:
            base_url (str): Your Kronos API endpoint, typically something like 'https://prefix.saashr.com/ta/rest/'
            api_key (str): Found in your account settings, your alphanumeric API key
            username (str): The username of your Kronos account or service account
            password (_type_): The password assigned to the username's account
            company (str): Your company short name, found in account settings or your original url
        """
        self.base_url = base_url
        self._api_key = api_key.lower()
        self.username = username.lower()
        self._password = password
        self.company = company

class kronos_credentials:
    def __init__(self, token: str, expiry_time: float):
        self._token = token
        self.expiry_time = expiry_time
    
    def print(self):
        print(f"Token: {self._token}, Expiry Time: {self.expiry_time}")
        
    def create_blank(self):
        self.token = ""
        self.expiry_time = 0
        
    def update(self, token: str, expiry_time: float):
        self._token = token
        self.expiry_time = expiry_time

def authenticate(kronos_endpoint):
    """Makes a call to the login endpoint to authenticate to UKG Workforce Ready and returns a token and expiry time

    Args:
        kronos_endpoint (kronos_endpoint): A kronos_endpoint object containing the base_url, api_key, username, password, and company

    Raises:
        Exception: Upon failure to login, an exception is raised

    Returns:
        kronos_credentials: A kronos_credentials object containing the token and expiry time
    """
    login_url = kronos_endpoint.base_url + "v1/login"
    credentials = {
        "credentials": {
            "username": kronos_endpoint.username,
            "password": kronos_endpoint.password,
            "company": kronos_endpoint.company
        }
    }
    login_headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_endpoint.api_key
    }

    # make a rest post call to login_url using the headers
    login = requests.post(login_url, headers=login_headers, json=credentials)

    # print request status code
    print(f"Status Code: {login.status_code}")

    if login.status_code != 200:
        raise Exception("Login failed")
    else:
        print("Login successful")
        # get the response
        response = login.json()
        # get the token from the response json
        token = response["token"]
        print(token)
        # record current system time
        curr_time = time.time()
        # response returns a ttl (time to live) in milliseconds
        # calculate expiry time by adding ttl to current time
        expiry_time = curr_time + response["ttl"]/1000
        print(f"Authentication complete. Token expires at {expiry_time}")
    return kronos_credentials(token, expiry_time)


def refresh_token(kronos_endpoint, kronos_credentials):
    """Refreshes the token to allow continued use of the API.

    Args:
        kronos_endpoint (kronos_endpoint): an instance of the `kronos_endpoint` class, containing the API endpoint details.
        kronos_credentials (kronos_credentials): an instance of the `kronos_credentials` class, containing the API key and the current token.

    Returns:
        kronos_credentials: an updated instance of the `kronos_credentials` class, with a refreshed token and a new expiry time.

    Raises:
        Exception: if the refresh request returns a non-200 status code, indicating a failure to refresh the token.
    """
    url = kronos_endpoint.base_url + "v1/refresh-token"
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_endpoint.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}"
    }
    refresh = requests.get(url, headers=headers)

    if refresh.status_code != 200:
        print(f"Status Code: {refresh.status_code}")
        raise Exception("Refresh failed")
    else:
        print("Refresh successful")
        token = refresh.json()["token"]
        expiry_time = time.time() + refresh.json()["ttl"]/1000
    kronos_credentials = kronos_credentials.update(token, expiry_time)


def check_token(kronos_endpoint, kronos_credentials):
    """Checks the current time against the token's expiry time and refreshes the token if necessary.

    Args:
        kronos_endpoint (kronos_endpoint): an instance of the `kronos_endpoint` class
        kronos_credentials (kronos_credentials): an instance of the `kronos_credentials` class

    Returns:
        kronos_credentials (kronos_credentials): an updated instance of the `kronos_credentials` class

    """
    # check if current time is greater than expiry time
    _75_percent = kronos_credentials.expiry_time*0.75
    # add "Authorization": f"Bearer {token}" to headers
    if time.time() > kronos_credentials.expiry_time:
        kronos_credentials = authenticate(kronos_endpoint)
        kronos_credentials = kronos_credentials.update(kronos_credentials.token, kronos_credentials.expiry_time)
    if time.time() > _75_percent:
        refresh_token(kronos_endpoint, kronos_credentials)

    