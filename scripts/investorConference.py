import requests
import json 
from bs4 import BeautifulSoup
import pandas as pd

def get_live_meetings():
    # 這是 IR 平台法說會的頁面，內容呈現清晰表格
    url = "https://irengage.taiwanindex.com.tw/conferenceList"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找表格
        table = soup.find('table')
        # 利用 pandas 直接讀取表格，這是處理 HTML 表格最穩定的方式
        df = pd.read_html(str(table))[0]

        # 篩選你需要的欄位（日期與公司）
        # 假設表格欄位名稱為：日期、時間、公司、地點...
        # 這裡根據網站結構進行清理
        result = df[['日期', '公司']].copy()
        
        # 將 DataFrame 轉成 list of dict
        output_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company_list": result,
        }


        import os
        os.makedirs("src/data", exist_ok=True)  # 確保資料夾存在
        with open("src/data/data_meetings.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print("檔案寫入成功:", os.path.exists("src/data/data_meetings.json"))

        return result

    except Exception as e:
        print(f"無法自動獲取清單: {e}")
        return None

# 執行
meetings_df = get_live_meetings()
if meetings_df is not None:
    print(meetings_df.to_string(index=False))