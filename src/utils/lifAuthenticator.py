import requests

auth_url = None

def set_auth_url(url):
    global auth_url
    auth_url = url

def verify_token(username, token):
    # Gets response from auth server
    status = requests.get(f"{auth_url}/verify_token/{username}/{token}")
    response_status = status.json()

    # Checks the response from auth server
    if response_status['Status'] == "Successful":
        return True
    
    else: 
        return False
