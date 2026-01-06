# Avatars
This repo includes two methods for managing the avatar images in Blackboard.</br>
Here is the (new) help page for Avatars: https://help.anthology.com/blackboard/administrator/en/user-management/avatars.html</br>
</br>
## BATCH:</br>
Blackboard supports a method of bundling avatar images in a .zip package and uploading in bulk.
The older help page for batch is here: https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars#:~:text=Upload%20system%20generated%20avatars</br>
I have created Python and Powershell scripts to read a csv with key values and file names to create .zip packages for manual upload.<br>
</br>
## API REST TOOL:
A newer addition to this repo is a REST-based avatar manager built with Python. It includes:
- A command-line interface (`main.py`) for bulk avatar upload and clearing.
- A Streamlit GUI (`app.py`) for interactive avatar management.
- Utility modules for authentication and API interaction (`auth.py`, `api.py`).
