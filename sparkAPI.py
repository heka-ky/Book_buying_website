# coding: utf-8
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from urllib.parse import urlparse, urlencode
import pytz
import websocket



class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        parsed_url = urlparse(gpt_url)
        self.host = parsed_url.netloc
        self.path = parsed_url.path
        self.gpt_url = gpt_url

    def create_url(self):
        # 生成 RFC 7231 时间格式
        now = datetime.now(pytz.utc)
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 构造签名原始字符串
        signature_origin = f"host: {self.host}\n" \
                           f"date: {date}\n" \
                           f"GET {self.path} HTTP/1.1"

        # 使用 hmac-sha256 计算签名
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')

        # 构造 Authorization 字符串
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", ' \
                               f'headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        # 构造最终URL
        params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return f"{self.gpt_url}?{urlencode(params)}"


def on_message(ws, message):
    data = json.loads(message)
    if data["header"]["code"] != 0:
        print(f'错误: {data["header"]["code"]}, {data["header"]["message"]}')
        ws.close()
    else:
        content = data["payload"]["choices"]["text"][0]["content"]
        print(content, end='')
        if data["payload"]["choices"]["status"] == 2:
            ws.close()


def on_error(ws, error):
    print("### 错误:", error)


def on_close(ws, close_status_code, close_reason):
    print(f"### 连接关闭: 状态码={close_status_code}, 原因={close_reason}")


def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws):
    data = json.dumps({
        "header": {
            "app_id": ws.appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": ws.domain,
                "max_tokens": 4096,
                "temperature": 0.7  # 可选参数
            }
        },
        "payload": {
            "message": {
                "text": [
                    {
                        "role": "user",
                        "content": ws.query
                    }
                ]
            }
        }
    })
    ws.send(data)


def main(appid, api_secret, api_key, Spark_url, domain, query):
    ws_param = Ws_Param(appid, api_key, api_secret, Spark_url)
    # websocket.enableTrace(True)  # 开启调试日志

    ws = websocket.WebSocketApp(
        ws_param.create_url(),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # 添加用户数据
    ws.appid = appid
    ws.domain = domain
    ws.query = query

    # 启动 WebSocket 连接
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    main(
        appid="8f79b10c",
        api_secret="YzI1OGRiZTBkZjQ5OTA0NWIzMmNjOTE4",
        api_key="6adc05b5734fd50f3debd7245796f889",
        Spark_url="wss://spark-api.xf-yun.com/v1.1/chat",
        domain="lite",
        query="给我写一篇100字的作文"
    )
