import json
from datetime import datetime
import yfinance as yf

def get_global_indices_perfect_final():
    print("正在啟動 yfinance 國際量化通道同步全球重要指數...")

    # 💡 定義商品，使用 STW=F (摩根台指期貨)
    mapping = {
        "^TWII": {"name": "台灣加權指數", "region": "台股"},
        "NQ=F": {"name": "美股-那斯達克期貨", "region": "美股"},
        "^N225": {"name": "日股-日經225指數", "region": "日股"},
        "^KS11": {"name": "韓股-韓國綜合指數", "region": "韓股"},
    }

    results = {}

    try:
        # 使用 yfinance 批量下載
        tickers = yf.Tickers(" ".join(mapping.keys()))

        # 使用 .items() 確保 sym 和 info 能正確對應
        for sym, info in mapping.items():
            region = info["region"]
            name = info["name"]

            ticker_info = tickers.tickers[sym].info

            price = (
                ticker_info.get("regularMarketPrice")
                or ticker_info.get("currentPrice")
                or ticker_info.get("navPrice")
                or 0.0
            )
            prev_close = ticker_info.get("previousClose") or price

            change = price - prev_close
            change_rate = (change / prev_close) * 100 if prev_close else 0.0
            trade_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            signal = "🔺" if change > 0 else ("🔻" if change < 0 else "⚪")

            results[region] = {
                "symbol": sym,
                "item_name": name,
                "current_price": round(price, 2),
                "price_change": round(change, 2),
                "price_change_percent": f"{change_rate:.2f}%",
                "status_signal": signal,
                "last_trade_time": trade_time,
            }

        print(f"🎉 成功抓取全球 {len(results)} 項關鍵指數動態！")
        return results

    except Exception as e:
        print(f"❌ 國際量化通道發生非預期錯誤: {e}")
        return None

def main():
    print("=== 全球指數自動化抓取  ===")

    market_data = get_global_indices_perfect_final()

    if not market_data or len(market_data) == 0:
        print("❌ 數據獲取失敗。")
        return

    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market_indices": market_data,
    }

    with open("data/data_global.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("\n================== 📊 全球市場即時戰報 ==================")
    for region, info in market_data.items():
        print(
            f"【{region}】{info['item_name']:<14} | 報價: {info['current_price']:<9} | 漲跌: {info['status_signal']}{abs(info['price_change']):<6} ({info['price_change_percent']})"
        )
    print("=========================================================")
    print("💾 完整數據已同步寫入 data_global.json")

if __name__ == "__main__":
    main()