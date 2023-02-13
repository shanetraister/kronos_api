# UKG Workforce Ready API Tools

A Python package for accessing, downloading, and writing data to and from a UKG Workforce Ready instance.

## Features
- Authenticate with UKG Workforce Ready using API keys
- Download data from UKG Workforce Ready
- Write data to UKG Workforce Ready
- Works with Python 3.x

## Installation

To install the package, use pip:



## Usage

The package provides the following modules for interacting with UKG Workforce Ready:

- `authenticate`: Contains functions and classes for authentication using API keys
- `download`: Contains functions for downloading data from UKG Workforce Ready
- `write`: Contains functions for writing data to UKG Workforce Ready

Here is an example of how to use the package:

```python
from ukgwr-api-tools import authentication, download_reports

# Set your kronos environment with an endpoint class object
kronos_endpoint = kronos_endpoint(
    base_url = "https://prefix.saashr.com/ta/rest/",
    api_key = "your_api_key",
    username = "your_username",
    password = "your_password",
    company = "1234567"
)

# Pass your endpoint to the authentication function and return your credentials
kronos_credentials = authentication.authenticate(kronos_endpoint)

# Find the report(s) you want to download
report_name = download_reports.get_report_names(kronos_endpoint, kronos_credentials, type="Saved")

# Then download the named report
report = download_reports.get_report(kronos_endpoint, kronos_credentials, report_name, report_scope="saved")
```

## Contributing
If you are interested in contributing to the project, please take a look at the contributing guidelines.

## License
The package is licensed under the GNU GPL3.0 license.