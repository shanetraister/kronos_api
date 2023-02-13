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

- `authenticate`: Contains functions for authentication using API keys
- `download`: Contains functions for downloading data from UKG Workforce Ready
- `write`: Contains functions for writing data to UKG Workforce Ready

Here is an example of how to use the package:

```python
import ukgwr-api-tools

# Authenticate with UKG Workforce Ready
ukgwr-api-tools.authenticate.authenticate_ukgwr()

# Download data from UKG Workforce Ready
data = ukgwr-api-tools.download.download_data()

# Write data to UKG Workforce Ready
ukgwr-api-tools.write.write_data(data)
```

## Contributing
If you are interested in contributing to the project, please take a look at the contributing guidelines.

## License
The package is licensed under the GNU GPL3.0 license.