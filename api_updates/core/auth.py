import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token(host):
    key = os.getenv("KEY")
    secret = os.getenv("SECRET")
    url = f"{host}/learn/api/public/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, auth=(key, secret))
    response.raise_for_status()
    return response.json().get("access_token")