import requests

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
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json().get("id")

def apply_avatar(host, token, user_id, upload_id):
    """
    Applies the uploaded avatar to the user using the upload ID.
    """
    url = f"{host}/learn/api/public/v1/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "avatar": {
            "source": "uploaded",
            "uploadId": upload_id
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()