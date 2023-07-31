from json import load
import os

directory = os.path.dirname(os.path.relpath(__file__))

def config(credentials_path=os.path.join(directory, 'openai_key.json')):
    """Function allowing to retrieve the open ai key.

    Args:
        credentials_path (str, optional): Credentials path. Defaults to './openai_key.json').

    Returns:
        str: OpenAI key.
    """
    if os.path.exists(credentials_path):
        content = load(open(credentials_path))
        key = content['openai_key']
        return key
    
    else:
        raise ValueError("The credentials json file cannot be found.")