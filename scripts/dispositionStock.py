import json
import re
from datetime import datetime
from curl_cffi import requests
import pandas as pd

def get_all_disposal_from_broker():
    print("正在同步上市處置股...")
    url = "https://www.twse.com.tw/zh/announcement/punish?response=json"
    results = []
    today = datetime.now()
    try:
        res = requests.get(url, impersonate="chrome", timeout=15)
        if res.status_code == 200:
            rows = res.json().get("data", [])
            for row in rows:
                if len(row) < 9: continue
                # 統一欄位命名
                results.append({
                    "market": "上市",
                    "code": row[2].strip(),
                    "name": row[3].strip(),
                    "start_date": row[6].split('~')[0].strip(),
                    "end_date": row[6].split('~')[1].strip() if '~' in row[6] else row[6].strip(),
                    "condition": row[5].strip(),
                    "measures": row[7].strip(),
                    "details": row[8].strip(),
                    "full_period": row[6].strip()
                })
        print(f"成功同步上市處置股: {len(results)} 檔")
    except Exception as e:
        print(f"上市抓取異常: {e}")
    return results

def get_tpex_disposal():
    print("正在同步上櫃處置股...")
    url = "https://www.tpex.org.tw/openapi/v1/tpex_disposal_information"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = r.json()
        results = []
        for item in data:
            # 民國轉西元
            roc_date = item.get("Date", "")
            ad_date = f"{int(roc_date[:3])+1911}/{roc_date[3:5]}/{roc_date[5:]}" if len(roc_date)>=7 else roc_date

            # 統一與上市相同的欄位格式
            results.append({
                "market": "上櫃",
                "code": item.get("SecuritiesCompanyCode", ""),
                "name": item.get("CompanyName", ""),
                "start_date": ad_date,
                "end_date": "請見詳情",
                "condition": "櫃買中心公告",
                "measures": item.get("DispositionPeriod", ""),
                "details": item.get("DispositionReasons", ""),
                "full_period": item.get("DispositionPeriod", "")
            })
        print(f"成功同步上櫃處置股: {len(results)} 檔")
        return results
    except Exception as e:
        print(f"上櫃抓取異常: {e}")
        return []

def main():
    print("=== 台灣股市處置股自動化系統 ===")

    # 1. 取得兩份統一格式的列表
    list1 = get_all_disposal_from_broker()
    list2 = get_tpex_disposal()
    all_disposal = list1 + list2

    # 2. 打包結構
    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disposition_count": len(all_disposal),
        "disposition_list": all_disposal,
    }

    # 3. 輸出 JSON
    with open("src/data/data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 完美過關！共整合 {len(all_disposal)} 檔處置股，已順利寫入 data.json")

if __name__ == "__main__":
    main()