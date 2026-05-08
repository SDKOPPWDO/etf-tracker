from http.server import BaseHTTPRequestHandler
import urllib.request
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://finance.yahoo.com",
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse symbol from path: /api/quote?symbol=SMH
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        symbol = qs.get("symbol", ["SMH"])[0].upper()

        try:
            # Current price
            quote_url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
            quote_data = fetch(quote_url)
            meta = quote_data["chart"]["result"][0]["meta"]
            close = meta.get("regularMarketPrice") or meta.get("chartPreviousClose")
            prev  = meta.get("chartPreviousClose", close)
            change = close - prev
            change_pct = (change / prev * 100) if prev else 0

            # 5Y history for ATH
            hist_url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5y"
            hist_data = fetch(hist_url)
            closes     = [x for x in hist_data["chart"]["result"][0]["indicators"]["quote"][0]["close"] if x]
            timestamps = hist_data["chart"]["result"][0]["timestamp"]
            ath        = max(closes)
            ath_idx    = closes.index(ath)
            ath_ts     = timestamps[ath_idx]

            import datetime
            ath_date = datetime.datetime.utcfromtimestamp(ath_ts).strftime("%Y-%m-%d")

            result = {
                "symbol": symbol,
                "close": round(close, 4),
                "prev_close": round(prev, 4),
                "change": round(change, 4),
                "change_pct": round(change_pct, 4),
                "ath": round(ath, 4),
                "ath_date": ath_date,
            }
            body = json.dumps(result).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            err = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(err)

    def log_message(self, *args):
        pass
