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

try:
    print("\n[INFO] Attempting to CREATE a new spreadsheet named 'Test-Bot-Sheet'...")
    new_sheet = client.create('Test-Bot-Sheet')
    print("[SUCCESS] Successfully created a new sheet!")
    print("Please check your Google Drive. You should see a file named 'Test-Bot-Sheet'.")

    # As a bonus, let's share it
    new_sheet.share('giridharshyam@gmail.com', perm_type='user', role='writer')
    print("I also shared it with your email: giridharshyam@gmail.com")

except Exception as e:
    print(f"\n[ERROR] The create test failed: {e}")
    print("This indicates a deeper problem with the API permissions on the Google Cloud project.")