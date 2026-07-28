import gspread
from google.oauth2.service_account import Credentials
import json
import os
import sys
from datetime import datetime

# ========================
# ดึง credentials จาก Environment Variable (ปลอดภัย)
# ========================
SHEET_ID = "1GyYgIOJQjQPuAMWPVRB8TI_C-3KZsBvbV8R_HByFH_8"
SHEET_NAME = "Summary_Daily"

def get_sheet_data():
    """ดึงข้อมูลจาก Google Sheet"""
    try:
        # อ่าน SERVICE_ACCOUNT_JSON จาก Environment Variable
        service_account_json = os.environ.get('SERVICE_ACCOUNT_JSON')
        
        if not service_account_json:
            print("❌ Error: SERVICE_ACCOUNT_JSON not found in environment", file=sys.stderr)
            return None
        
        # Parse JSON string
        creds_dict = json.loads(service_account_json)
        
        # สร้าง Credentials จาก dictionary
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        # เชื่อมต่อ Google Sheets
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        data = sheet.get_all_values()
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in SERVICE_ACCOUNT_JSON - {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None

def save_to_json(data, filename='data.json'):
    """บันทึกข้อมูลเป็น JSON"""
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ Data saved to {filename}")
    else:
        print("❌ No data to save")

if __name__ == '__main__':
    print("🔄 Starting update process...")
    print("📊 Fetching data from Google Sheet...")
    
    data = get_sheet_data()
    
    if data:
        print("✅ Data retrieved successfully!")
        save_to_json(data)
        print("✨ Update completed!")
    else:
        print("❌ Failed to retrieve data")
        sys.exit(1)
