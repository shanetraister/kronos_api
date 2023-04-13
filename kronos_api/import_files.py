import requests
from datetime import datetime
from uuid import uuid4
from kronos_api.authentication import check_token
from io import StringIO
import pandas as pd

def import_employees(kronos_endpoint,kronos_credentials, df: pd.DataFrame = None, filepath = None, type: str = "100", format: str = ".csv", force_upload = True):
    """A function to leverage the import api to import an Employees template to Kronos. Use 100 for "Excel" format, 101 for "XML", and 209 for "Excel 2007". 

    Args:
        kronos_endpoint (kronos_endpoint): an instance of the `kronos_endpoint` class, containing the API endpoint details.
        kronos_credentials (kronos_credentials): an instance of the `kronos_credentials` class, containing the API key and the current token.
        df (pd.DataFrame): A pandas dataframe containing the data to be imported.
        type (str, optional): The type of file to import. Defaults to "100". Use 100 for "Excel" format, 101 for "XML", and 209 for "Excel 2007".
        format (str, optional): The format of the file to import. Defaults to "Excel". Use "Excel" for Excel 97-2003, "Excel 2007" for Excel 2007, and "XML" for XML.

    Returns:
        status_code: The status code of the request
    """    
    check_token(kronos_endpoint, kronos_credentials)

    # if df is not none, then we'll use that and format as csv, otherwise import the filepath and format as specified
    # TODO: Add support for other formats
    # TODO: Assert that either df or filepath exists, but not both and not neither
    # Add custom error for this type of error
    if df is not None:
        file_content = df.copy().to_csv(index=False)
    else:
        # Determine type of import from filepath format
        format = filepath.split(".")[-1]
        with open(filepath, "rb") as f:
            file_content = f.read()

    content_type = content_type_map.get(format)

    if content_type is None:
        raise ValueError(f"Unsupported file extension '{format}'")

    boundary = str(uuid4())
    
    headers = {
        "Content-Type": "application/json",
        "Api-Key": kronos_endpoint.api_key,
        "Authorization": f"Bearer {kronos_credentials.token}",
        "Accept": "application/json",
        "Content-Type": f"multipart/form-data; boundary={boundary}
        }

    content_type_map = {
        "csv": "text/csv",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "xml": "application/xml",
    }

    params = {
        "company_id": kronos_endpoint.company,
        "force_upload": force_upload,
    }

    url = kronos_endpoint.base_url + f"v1/import/{type}"
    # file_name = employees+today's date formatted as YYYYMMDD
    file_name = f"employees{datetime.today().strftime('%Y%m%d')}"
    
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f"Content-Type: {content_type}\r\n"
        f"\r\n"
    )

    if format == "csv" or format == "xml":
        body += file_content + f"\r\n"
        body_final = body.encode("utf-8")
    else:
        body = body.encode() + file_content + b"\r\n"
        body_final = body + f"--{boundary}--\r\n".encode()

    upload = requests.post(url, headers=headers, data=body_final, params=params)

    print(f"Getting {type} report names")
    if upload.status_code != 200:
        print(f"Status Code: {upload.status_code}")
        print(upload.content)
        print("Employee Import Failed")
    else:
        print("Employees Imported")
        return upload.status_code