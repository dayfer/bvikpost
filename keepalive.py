import requests
import time
from datetime import datetime

api_url = "https://temperature-ugdebiz6jq-uc.a.run.app"
#api_url = "http://127.0.0.1:5001/bvik-370610/us-central1/temperature"

def try_post(url):
    reportTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report =  { "reporter":"bvik1", "datetime":reportTime}
    print(report)
    try:
       response = requests.post(url, json=report)
    except requests.exceptions.RequestException as e:
       print("Cannot connect")
       print(e);
       # TODO: cancellation logic to return False
       return 5
    else:
       return 900

while True:
    timeout = try_post(api_url)
    print("sleep: " + str(timeout))
    time.sleep(timeout)

