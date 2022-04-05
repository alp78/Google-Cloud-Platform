import os
import json
import base64
from flask import Flask, request

app = Flask(__name__)

MESSAGES = []

@app.route('/', methods=['GET'])
def index():
    return 'PubSub Test /push /read'


@app.route('/read', methods=['GET'])
def read_message():
    try:
        message = MESSAGES.pop()
    except:
        return 'no more messages'
    
    return message.decode("utf-8")


@app.route('/push', methods=['POST'])
def get_message():
    
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])

    MESSAGES.append(payload)

    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
