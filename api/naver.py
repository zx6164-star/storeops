import urllib.request
from http.server import BaseHTTPRequestHandler

NAVER_CLIENT_ID     = "6BwAsws_xLfrSAbq2O_4"
NAVER_CLIENT_SECRET = "dRToUtjNC3"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = self.path.split("?q=")[-1] if "?q=" in self.path else ""
        url = f"https://openapi.naver.com/v1/search/book.json?query={query}&display=10"
        req = urllib.request.Request(url, headers={
            "X-Naver-Client-Id":     NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        })
        try:
            with urllib.request.urlopen(req) as res:
                data = res.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f'{{"error":"{str(e)}"}}'.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()
