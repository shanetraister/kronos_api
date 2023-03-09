from dateutil import parser

def convert_to_yyyymmdd(date_str):
    # List of common date formats to check
    date_formats = ['%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y', '%m-%d-%y']

    # Try to parse the date string using each format
    for date_format in date_formats:
        try:
            date_obj = parser.parse(date_str)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass

    # If none of the formats match, raise an error
    raise ValueError("Invalid date format")