import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]
SERVICE_ACCOUNT_FILE = 'service_account.json'

print("[INFO] Attempting to connect to Google...")
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(creds)
print("[INFO] Authentication successful.")

print("\n[INFO] Fetching list of all spreadsheets this bot can see...")
try:
    spreadsheet_list = client.list_spreadsheet_files()
    
    if not spreadsheet_list:
        print("\n[RESULT] The bot can't see ANY spreadsheets yet.")
        print("This confirms the sharing permission for 'Attendance' hasn't gone through.")
        print("Please wait 5 more minutes and try the main program again.")
        
    else:
        print("\n[RESULT] The bot can see the following spreadsheets:")
        file_names = []
        for s in spreadsheet_list:
            print(f"  - {s['name']}")
            file_names.append(s['name'])
    
        if "Attendance" in file_names:
            print("\n[SUCCESS] 'Attendance' is visible! The main script should work now.")
        else:
            print("\n[FAIL] 'Attendance' is NOT in the list. This means the sharing permission is still processing.")
            print("Please wait 5-10 minutes. It will work eventually.")

except Exception as e:
    print(f"\n[ERROR] An API error occurred: {e}")
    print("This might mean the Google Drive/Sheets APIs are not enabled correctly.")
    