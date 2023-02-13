import requests
# how to import the function check_token from kronos_auth.py?
from kronos_auth import check_token
from xml import xmltodict
import pandas as pd

# Do I need to require parameters like base_url, token, etc... if they're used in the function but defined globally?

def get_report_names(kronos_endpoint, kronos_credentials, type="Saved"):
    """A function to get the names of reports, either all reports or saved

    Args:
        kronos_endpoint (kronos_endpoint): an instance of the `kronos_endpoint` class, containing the API endpoint details.
        kronos_credentials (kronos_credentials): an instance of the `kronos_credentials` class, containing the API key and the current token.
        type (str, optional): Can be "All" or "Saved". All proivdes base reports, saved provides saved copies of reports. Defaults to "Saved".

    Returns:
        _type_: _description_
    """    
    kronos_credentials = check_token(kronos_endpoint, kronos_credentials)
    assert type in ["All", "Saved"], "type must be either 'All' or 'Saved'"
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_credentials.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/json",
        }

    params={"type": type}

    if type == "Saved":
        params = {"type": type, "other": True}

    url = kronos_endpoint.base_url + "v1/reports"

    reports = requests.get(url, headers=headers, params=params)
    all_reports = "Nothing's here"
    print(f"Getting {type} report names")
    if reports.status_code != 200:
        print(f"Status Code: {reports.status_code}")
        print(reports.content)
        print("Report failed")
    else:
        all_reports = reports
        print(f"Found {len(all_reports.json())} reports")
        return all_reports


def get_report(kronos_endpoint, kronos_credentials, report_name, report_scope: str = "saved"):
    kronos_credentials = check_token(kronos_endpoint, kronos_credentials)
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_credentials.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/json",
        }
    url = kronos_endpoint.base_url + "v1/report/" + report_scope + "/" + report_name
    
    report = requests.get(url, headers=headers)
    
    if report.status_code !=200:
        print(f"Status Code: {report.status_code}")
        # print(report.content)
        print(f"Failed to retrieve {report_name}")
    else:
        report = report.content
        dict_data = xmltodict.parse(report)
        body_data = dict_data["result"]["body"]
        body = [x['col'] for x in body_data['row']]

        header_data = dict_data["result"]["header"]
        header = [x['label'] for x in header_data['col']]
        
        df = pd.DataFrame(body, columns=header)
        print(f"Retrieved {report_name}")
        return report, df


# TODO: Get this working
# def get_report_with_filters(kronos_endpoint, kronos_credentials,report_name, filters):
#     kronos_credentials = check_token(kronos_endpoint, kronos_credentials)
#     headers = {
#         "Content-Type": "application/json",
#         "Api-Key": kronos_credentials.api_key,
#         "Authorization": f"Bearer {kronos_credentials.token}",
#         "Accept": "application/json",
#         }
#     report_id = report_name
#     url = kronos_endpoint.base_url + "v1/report/global/" + report_id
    
#     report = requests.get(url, headers=headers)
    
#     if report.status_code !=200:
#         print(f"Status Code: {report.status_code}")
#         # print(report.content)
#         print(f"Failed to retrieve {report_name}")
#     else:
#         report = report.content
#         dict_data = xmltodict.parse(report)
#         body_data = dict_data["result"]["body"]
#         body = [x['col'] for x in body_data['row']]

#         header_data = dict_data["result"]["header"]
#         header = [x['label'] for x in header_data['col']]
        
#         df = pd.DataFrame(body, columns=header)
#         print(f"Retrieved {report_name}")
#         return df


def get_report_metadata(kronos_endpoint, kronos_credentials, report_name):
    kronos_credentials = check_token(kronos_endpoint, kronos_credentials)
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_credentials.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/xml",
        }
    url = kronos_endpoint.base_url + "v1/report/global/" + report_name + "/metadata"
    
    report = requests.get(url, headers=headers)
    
    if report.status_code !=200:
        print(f"Status Code: {report.status_code}")
        # print(report.content)
        print(f"Failed to retrieve {report_name}")
    else:
        report = report.content
        dict_data = xmltodict.parse(report)
        # body_data = dict_data["result"]["body"]
        # body = [x['col'] for x in body_data['row']]

        # header_data = dict_data["result"]["header"]
        # header = [x['label'] for x in header_data['col']]
        
        # df = pd.DataFrame(body, columns=header)
        print(f"Retrieved {report_name}")
        return dict_data