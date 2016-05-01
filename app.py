from flask import Flask
from flask import request

import requests
import json
import re

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1466099631', # Channel ID
    'X-Line-ChannelSecret':'1255afe6c79053d174d67a6d3d310eb5', # Channel secre
    'X-Line-Trusted-User-With-ACL':'ue791aeb4fd39f39d9a9460e80bd07490' # MID (of Channel)
}

def post_event(to, content):
    msg = {
        'to': [to],
        'toChannel': 1383378250, # Fixed  value
        'eventType': "138311608800106203", # Fixed value
        'content': content
    }
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

def post_text(to, text):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)


commands = (
    (re.compile('ラッシャー', 0), lambda x: 'テメエコノヤロウ'),
    (re.compile('ダンカン', 0), lambda x:'バカヤロコノヤロウ'),
)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def hello():
    msgs = request.json['result']
    for msg in msgs:
        text = msg['content']['text']
        for matcher, action in commands:
            if matcher.search(text):
                response = action(text)
                break
        else:
            response = 'コマネチ'

        post_text(msg['content']['from'],response)

    return ''

if __name__ == "__main__":
    #context = ('cert/server.pem', 'cert/privkey.pem')
    #app.run(host = '0.0.0.0', port = 443, ssl_context = context, threaded = True, debug = True)
    app.run(host = '0.0.0.0', port = 8001, threaded = True, debug = True)
