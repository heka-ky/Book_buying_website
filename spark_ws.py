import base64, hashlib, hmac, json, ssl, time
from datetime import datetime
from urllib.parse import urlparse, urlencode
import websocket
import pytz

class WsParam:
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        parsed_url = urlparse(gpt_url)
        self.host = parsed_url.netloc
        self.path = parsed_url.path
        self.gpt_url = gpt_url

    def create_url(self):
        now = datetime.now(pytz.utc)
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        signature_origin = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode(), signature_origin.encode(), hashlib.sha256).digest()
        signature_base64 = base64.b64encode(signature_sha).decode()
        auth_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_base64}"'
        auth = base64.b64encode(auth_origin.encode()).decode()
        return f"{self.gpt_url}?{urlencode({'authorization': auth, 'date': date, 'host': self.host})}"

class SparkChat:
    def __init__(self, appid, api_secret, api_key, gpt_url, domain):
        self.appid = appid
        self.api_secret = api_secret
        self.api_key = api_key
        self.gpt_url = gpt_url
        self.domain = domain
        self.answer = ""

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["header"]["code"] != 0:
            self.answer = f"[错误]: {data['header']['message']}"
            ws.close()
        else:
            content = data["payload"]["choices"]["text"][0]["content"]
            self.answer += content
            if data["payload"]["choices"]["status"] == 2:
                ws.close()

    def on_error(self, ws, error):
        self.answer = f"[错误]: {error}"

    def on_close(self, ws, close_status_code, close_msg):
        pass

    def on_open(self, ws):
        body = {
            "header": {"app_id": self.appid, "uid": "user123"},
            "parameter": {"chat": {"domain": self.domain, "max_tokens": 2048, "temperature": 0.5}},
            "payload": {"message": {"text": [{"role": "user", "content": self.query}]}}
        }
        ws.send(json.dumps(body))

    def send(self, query):
        self.query = query
        url = WsParam(self.appid, self.api_key, self.api_secret, self.gpt_url).create_url()
        ws = websocket.WebSocketApp(url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.answer
