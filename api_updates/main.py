import argparse
import os
import logging
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
parser.add_argument('--action', choices=['Add', 'Clear'], default='Add', help='Action to perform on avatars')
args = parser.parse_args()

# Configure logging
log_level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prepend https:// to host
base_url = f"https://{args.host}"
logger.debug(f"Using host: {base_url}")
logger.debug(f"Avatar folder: {args.folder}")
logger.debug(f"Action: {args.action}")

# Get access token
try:
    access_token = get_access_token(base_url)
    logger.debug("Access token retrieved successfully.")
except Exception as e:
    logger.error(f"Failed to retrieve access token: {e}")
    exit(1)

# Process each image in the folder
for filename in os.listdir(args.folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        user_id = os.path.splitext(filename)[0]
        image_path = os.path.join(args.folder, filename)
        logger.info(f"Processing {filename} for user {user_id}")

        if not args.dry_run:
            try:
                if args.action == 'Add':
                    upload_id = upload_avatar(base_url, access_token, image_path)
                    result = apply_avatar(base_url, access_token, user_id, upload_id)
                    logger.info(f"Avatar applied for {user_id}: {result}")
                elif args.action == 'Clear':
                    result = apply_avatar(base_url, access_token, user_id, None)
                    logger.info(f"Avatar cleared for {user_id}: {result}")
            except Exception as e:
                logger.error(f"Error processing {user_id}: {e}")
        else:
            logger.info(f"Dry run: Skipping {args.action.lower()} for {user_id}")