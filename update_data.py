import gspread
from google.oauth2.service_account import Credentials
import json
import sys
from datetime import datetime

# ========================
# 1. ดึง SHEET_ID จาก Google Sheet ของคุณ
# ========================
# ที่ URL ของ Google Sheet: https://docs.google.com/spreadsheets/d/[SHEET_ID]/...
# SHEET_ID คือส่วนที่ยาว ๆ ตรงกลาง
SHEET_ID = "1GyYgIOJQjQPuAMWPVRB8TI_C-3KZsBvbV8R_HByFH_8"
SHEET_NAME = "Summary_Daily"  # ชื่อ sheet

def get_sheet_data():
    """ดึงข้อมูลจาก Google Sheet"""
    try:
        # ใช้ service account key (จะสร้างใน step ต่อไป)
        creds = Credentials.from_service_account_file(
            'service_account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        data = sheet.get_all_values()
        return data
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
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
    data = get_sheet_data()
    save_to_json(data)
