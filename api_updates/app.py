import streamlit as st
import os
import logging
from dotenv import load_dotenv
from core.auth import get_access_token
from core.api import upload_avatar, apply_avatar

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_stream = []

# Set page config
st.set_page_config(
    page_title="Blackboard Avatar Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Blackboard branding
st.markdown("""
    <style>
        body {
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton>button {
            background-color: #3b3f58;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #5a5f7a;
        }
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            background-color: #2a2a2a;
            color: white;
        }
        .stSelectbox>div>div {
            background-color: #2a2a2a;
            color: white;
        }
        .stCheckbox>div>label {
            color: #f0f0f0;
        }
        footer {
            visibility: hidden;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            color: #888;
            text-align: center;
            font-size: 0.8rem;
            padding: 0.5rem;
        }
    </style>
    <div class="footer">
        Blackboard Avatar Manager v1.0 | © 2025 Anthology Inc.
    </div>
""", unsafe_allow_html=True)

# Layout: 3 columns
left_col, mid_col, right_col = st.columns([1, 2, 4])

# Left: Configuration
with left_col:
    st.markdown("### Configuration")
    dry_run = st.checkbox("Dry Run Mode", value=True, help="Enable to simulate actions without making changes.")
    verbose = st.checkbox("Verbose Logging", value=False, help="Enable detailed logging output.")
    log_to_file = st.checkbox("Log to File", value=False, help="Save logs to a local text file.")

# Middle: Inputs
with mid_col:
    st.markdown("### Inputs")
    host = st.text_input("Blackboard Hostname", value="", help="Enter the Blackboard server hostname (e.g., blackboard.example.edu).")
    avatar_folder = st.text_input("Avatar Folder Path", value="./avatars", help="Path to the folder containing avatar images.")
    action = st.selectbox("Action", options=["Add", "Clear"], index=0, help="Choose whether to add or clear avatars.")
    run_button = st.button("Run Avatar Update")

# Right: Logs
with right_col:
    st.markdown("### Logs")
    log_container = st.empty()

def log_message(message, level="info"):
    log_stream.append(message)
    log_container.markdown("<div style='height:400px;overflow-y:auto'>" + "<br>".join(log_stream[-100:]) + "</div>", unsafe_allow_html=True)

# Summary counters
total_processed = 0
total_success = 0
total_skipped = 0
total_failed = 0

# Middle: Actions
with mid_col:
    if run_button:
        base_url = f"https://{host}"
        log_message(f"Using host: {base_url}")
        log_message(f"Avatar folder: {avatar_folder}")

        try:
            access_token = get_access_token(base_url)
            log_message("Access token retrieved successfully.", "success")
        except Exception as e:
            log_message(f"Failed to retrieve access token: {e}", "error")
            st.stop()

        if not os.path.isdir(avatar_folder):
            log_message("Invalid folder path.", "error")
            st.stop()

        if log_to_file:
            log_filename = "avatar_update_log.txt"
            with open(log_filename, "w") as log_file:
                log_file.write("Blackboard Avatar Update Log\n\n")

        for filename in os.listdir(avatar_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                total_processed += 1
                user_id = os.path.splitext(filename)[0]
                image_path = os.path.join(avatar_folder, filename)
                log_message(f"Processing {filename} for user {user_id}")

                if not dry_run:
                    try:
                        if action == "Add":
                            upload_id = upload_avatar(base_url, access_token, image_path)
                            result = apply_avatar(base_url, access_token, user_id, upload_id)
                            log_message(f"Avatar applied for {user_id}: {result}", "success")
                            total_success += 1
                            if log_to_file:
                                with open(log_filename, "a") as log_file:
                                    log_file.write(f"Avatar applied for {user_id}: {result}\n")
                        elif action == "Clear":
                            result = apply_avatar(base_url, access_token, user_id, None)
                            log_message(f"Avatar cleared for {user_id}: {result}", "success")
                            total_success += 1
                            if log_to_file:
                                with open(log_filename, "a") as log_file:
                                    log_file.write(f"Avatar cleared for {user_id}: {result}\n")
                    except Exception as e:
                        log_message(f"Error processing {user_id}: {e}", "error")
                        total_failed += 1
                        if log_to_file:
                            with open(log_filename, "a") as log_file:
                                log_file.write(f"Error processing {user_id}: {e}\n")
                else:
                    log_message(f"Dry run: Skipping {action.lower()} for {user_id}", "info")
                    total_skipped += 1
                    if log_to_file:
                        with open(log_filename, "a") as log_file:
                            log_file.write(f"Dry run: Skipping {action.lower()} for {user_id}\n")

        # Display summary report
        st.markdown("### Summary Report")
        st.success(f"Total Processed: {total_processed}")
        st.info(f"Successful: {total_success}")
        st.warning(f"Skipped (Dry Run): {total_skipped}")
        if total_failed > 0:
            st.error(f"Failed: {total_failed}")
        else:
            st.success("No failures encountered.")