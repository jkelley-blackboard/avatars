import argparse
import os
from dotenv import load_dotenv
from core.auth import get_access_token
from core.api import upload_avatar, apply_avatar

# Load credentials from .env
load_dotenv()

# Set up CLI arguments
parser = argparse.ArgumentParser(description='Update user avatars via Blackboard API')
parser.add_argument('--host', required=True, help='Blackboard hostname (e.g., your.blackboard.com)')
parser.add_argument('--folder', required=True, help='Path to folder containing avatar images')
parser.add_argument('--dry-run', action='store_true', help='Simulate actions without making API calls')
parser.add_argument('--verbose', action='store_true', help='Enable detailed logging')
args = parser.parse_args()

# Prepend https:// to host
base_url = f"https://{args.host}"

if args.verbose:
    print(f"Using host: {base_url}")
    print(f"Avatar folder: {args.folder}")

# Get access token
access_token = get_access_token(base_url)

# Process each image in the folder
for filename in os.listdir(args.folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        user_id = os.path.splitext(filename)[0]
        image_path = os.path.join(args.folder, filename)

        if args.verbose:
            print(f"Processing {filename} for user {user_id}")

        if not args.dry_run:
            try:
                # Upload image and get uploadId
                upload_id = upload_avatar(base_url, access_token, image_path)

                # Apply avatar using uploadId
                result = apply_avatar(base_url, access_token, user_id, upload_id)

                if args.verbose:
                    print(f"Avatar applied for {user_id}: {result}")
            except Exception as e:
                print(f"Error processing {user_id}: {e}")
