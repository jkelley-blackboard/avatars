# Blackboard Avatar Manager

**Version:** 1.0  
**Author:** Jeff Kelley  
**© 2025 Anthology Inc.**

## Overview

This project provides both a command-line interface (CLI) and a Streamlit-based graphical user interface (GUI) for managing user avatars in Blackboard via the REST API. It supports bulk operations to **add** or **clear** avatars using images stored in a local folder. The tool is designed for administrators and developers working with Blackboard SaaS deployments.

Please note that the process of adding or updating an avatar image to a user has two steps.  You must first make a POST request to /learn/api/public/v1/uploads to add the file to Blackboard and then use the ID number in the response to attach the uploaded file to the user record.
---

## Features

- Upload avatars for multiple users using image filenames as user IDs.
- Clear existing avatars and revert to default.
- Dry-run mode for safe testing.
- Verbose logging and optional log-to-file.
- Streamlit GUI for interactive use.
- Modular design with reusable authentication and API utilities.

---

## Project Structure

```
├── app.py              # Streamlit GUI
├── main.py             # CLI interface
├── core/
│   ├── auth.py         # Blackboard OAuth2 token retrieval
│   └── api.py          # Avatar upload and apply functions
├── .env                # Contains KEY and SECRET for API access
├── avatars/            # Folder containing avatar images
```

---

## Setup

### 1. Environment Variables

Create a `.env` file in the root directory with the following contents:

```env
KEY=your_blackboard_application_key
SECRET=your_blackboard_application_secret
```

### 2. Install Dependencies

```bash
pip install streamlit python-dotenv requests
```

---

## Usage

### CLI (`main.py`)

```bash
python main.py --host your.blackboard.com --folder ./avatars --action Add --dry-run --verbose
```

#### Arguments:
- `--host`: Blackboard hostname (e.g., `your.blackboard.com`)
- `--folder`: Path to folder containing avatar images
- `--action`: `Add` or `Clear`
- `--dry-run`: Simulate actions without making API calls
- `--verbose`: Enable detailed logging

---

### GUI (`app.py`)

```bash
streamlit run app.py
```

#### GUI Options:
- **Dry Run Mode**: Simulates actions without making changes.
- **Verbose Logging**: Enables detailed logs.
- **Log to File**: Saves logs to `avatar_update_log.txt`.
- **Host Input**: Blackboard hostname.
- **Avatar Folder Path**: Path to image folder.
- **Action**: Add or Clear avatars.

---

## Utility Modules

### `auth.py`

Handles OAuth2 token retrieval using client credentials.

```python
get_access_token(host)
```

Returns an access token using the `KEY` and `SECRET` from `.env`.

---

### `api.py`

#### `upload_avatar(host, token, image_path)`
Uploads an image to Blackboard and returns the upload ID.

#### `apply_avatar(host, token, user_id, upload_id)`
Applies the uploaded avatar to a user. If `upload_id` is `None`, it clears the avatar and reverts to default.

---

## Avatar Image Naming Convention

Each image file should be named using the Blackboard user ID:

```
_123_1.jpg → applies to user ID _123_1
```

Supported formats: `.jpg`, `.jpeg`, `.png`

---

## Logging

- Logs are printed to console or Streamlit interface.
- If enabled, logs are saved to `avatar_update_log.txt`.

---

## License

This project is proprietary and intended for internal use by Anthology Inc.
