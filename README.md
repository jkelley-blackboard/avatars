# avatars
scripts and stuff to help manage Blackboard avatars</br>
The plan is to capture helpful code for both creating batch .zip files AND for using REST API</br>
</br>
## BATCH:</br>
The help page for batch is here: https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars#:~:text=Upload%20system%20generated%20avatars</br>
Loaded Python and Powershell scripts to read a csv with key values and file names to create .zip packages to upload.<br>
</br>
## API REST TOOL:
A new addition to this repo is a REST-based avatar manager built with Python. It includes:
- A command-line interface (`main.py`) for bulk avatar upload and clearing.
- A Streamlit GUI (`app.py`) for interactive avatar management.
- Utility modules for authentication and API interaction (`auth.py`, `api.py`).
