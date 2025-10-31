import requests
import logging

def upload_avatar(host, token, image_path):
    """
    Uploads the image to temporary storage and returns the file upload ID.
    """
    url = f"{host}/learn/api/public/v1/uploads"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    with open(image_path, "rb") as image_file:
        files = {
            "file": image_file
        }
        logging.debug(f"Uploading avatar:\n URL: {url}\n Headers: {headers}\n File: {image_path}")
        response = requests.post(url, headers=headers, files=files)
        logging.debug(f"Upload response:\n Status: {response.status_code}\n Body: {response.text}")
        response.raise_for_status()
        return response.json().get("id")

def apply_avatar(host, token, user_id, upload_id):
    """
    Applies the uploaded avatar to the user using the upload ID,
    or clears the avatar if upload_id is None.
    """
    url = f"{host}/learn/api/public/v1/users/{user_id}?fields=avatar"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if upload_id:
        data = {
            "avatar": {
                "uploadId": upload_id
            }
        }
    else:
        data = {
            "avatar": {
                "source": "Default"
            }
        }

    logging.debug(f"Applying avatar:\n URL: {url}\n Headers: {headers}\n Payload: {data}")
    response = requests.patch(url, headers=headers, json=data)
    logging.debug(f"Apply response:\n Status: {response.status_code}\n Body: {response.text}")
    response.raise_for_status()
    return response.json()