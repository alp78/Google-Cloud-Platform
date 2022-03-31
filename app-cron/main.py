from flask import Flask, request
import random
import json
from datetime import datetime as dt

  
devices = ['Samsung Galaxy S9', 
            'Samsung Galaxy S8', 
            'Samsung Galaxy S7', 
            'Samsung Galaxy S7 Edge',
            'Samsung Galaxy S6',
            'Nexus 6P',
            'Sony Xperia XZ',
            'Sony Xperia Z5',
            'HTC One X10',
            'HTC One M9',
            'Apple iPhone XR',
            'Apple iPhone XS',
            'Apple iPhone X',
            'Apple iPhone 8',
            'Apple iPhone 7',
            'Apple iPhone 6',
            'Google Pixel C',
            'Mac OS X',
            'Windows 7',
            'Windows 10',
            'Microsoft Lumia 950',
            'Sony Xperia Z4']


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate():
  if request.method == 'GET':
    time = dt.now()
    time = time.strftime("%m/%d/%Y %H:%M:%S")
    client_id = random.randint(1, 1000)
    device = random.choices(devices, k=1)
    view_time = random.randint(1, 1000)
    
    d = {'client_id': client_id,
        'device': device,
        'view_time': view_time,
        'time': time}
    
    print(request)
    
    return json.dumps(d, indent=4)
  
  data = request
  return data

if __name__ == '__main__':
  app.run()
