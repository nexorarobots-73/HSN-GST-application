import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_access_token():
    """Get Microsoft Graph API access token using MSAL"""
    try:
        client_id = os.getenv("CLIENT_ID")
        authority = os.getenv("AUTHORITY")
        scopes = os.getenv("SCOPES", "User.Read Files.ReadWrite.AppFolder").split()
        
        app = PublicClientApplication(client_id=client_id, authority=authority)
        
        # Try to get token silently first (from cache)
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(scopes=scopes, account=accounts[0])
            if result:
                return result.get("access_token")
        
        # If silent acquisition fails, use interactive login
        result = app.acquire_token_interactive(scopes=scopes)
        if "access_token" in result:
            return result["access_token"]
        else:
            print(f"Error: {result.get('error')}")
            print(f"Description: {result.get('error_description')}")
            return None
    except Exception as e:
        print(f"Error getting access token: {str(e)}")
        return None

def upload_to_onedrive(local_path, onedrive_filename):
    """Upload a file to OneDrive App folder"""
    try:
        token = get_access_token()
        if not token:
            return False
            
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/csv"
        }
        
        # Upload to app folder
        url = f"https://graph.microsoft.com/v1.0/me/drive/special/approot:/{onedrive_filename}:/content"
        
        with open(local_path, "rb") as f:
            response = requests.put(url, headers=headers, data=f)
            
        if response.status_code in (200, 201):
            return True
        else:
            print(f"Upload failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error uploading to OneDrive: {str(e)}")
        return False

def download_from_onedrive(onedrive_filename, local_path):
    """Download a file from OneDrive App folder"""
    try:
        token = get_access_token()
        if not token:
            return False
            
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Download from app folder
        url = f"https://graph.microsoft.com/v1.0/me/drive/special/approot:/{onedrive_filename}:/content"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Download failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error downloading from OneDrive: {str(e)}")
        return False