import requests
import json 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def get_live_meetings():
    url = "https://irengage.taiwanindex.com.tw/conferenceList"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找 table
        table = soup.find('table')
        if table is None:
            raise Exception("找不到 table")

        # pandas 讀取表格
        from io import StringIO
        df = pd.read_html(StringIO(str(table)))[0]

        # 篩選欄位
        result = df[['日期', '公司']].copy()

        # 轉成 list of dict
        output_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company_list": result.to_dict(orient="records"),
        }

        # 確保資料夾存在
        os.makedirs("data", exist_ok=True)

        # 寫入 JSON
        with open("data/data_meetings.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print("檔案寫入成功:", os.path.exists("data/data_meetings.json"))

        return result

    except Exception as e:
        print(f"無法自動獲取清單: {e}")
        return None

# 執行
meetings_df = get_live_meetings()
if meetings_df is not None:
    print(meetings_df.to_string(index=False))