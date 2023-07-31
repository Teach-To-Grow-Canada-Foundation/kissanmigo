import ee
from json import load
import os

directory = os.path.dirname(os.path.relpath(__file__))

def config(credentials_path=os.path.join(directory, 'gee_credentials.json')):
    """Function allowing to retrieve google earth engine credentials.

    Args:
        credentials_path (str, optional): Path containing a credentials json file. Defaults to './gee_credentials.json').

    Returns:
        ee: Configured earth engine object.
    """
    if os.path.exists(credentials_path):
        content = load(open(credentials_path))
        service_account = content['client_email']
        credentials = ee.ServiceAccountCredentials(service_account, credentials_path)
        ee.Initialize(credentials)
        
        return ee
    
    else:
        raise ValueError("The entered path to google earth engine credentials cannot be found.")