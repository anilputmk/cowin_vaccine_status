import pync
# https://pypi.org/project/pync/
import schedule
# https://pypi.org/project/schedule/
import time
import os, sys
from daemonize import Daemonize
from datetime import datetime
import notify2

import requests


baseUrl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=288&date='

def demon_notify():
    # result = True
    # try:
    #     notify2.init("Bandwidth")
    #     mess = notify2.Notification("Bandwidth","",'')
    #     mess.set_urgency(2)
    #     mess.set_timeout(0)
    #     mess.show()
    # except:
    #     result = False
    # return result
    pass

def job():
    # print("Running job")
    # pync.notify('Hello World')
    month=6
    day=1
    print(f"Day = {day}, month={month}")
    
  
    headers={
      'Accept-Language': 'hi_IN',
      'accept': 'application/json',
      'Host': 'cdn-api.co-vin.in',
      'User-Agent':'PostmanRuntime/7.26.8'
    }

    while True:
      url = f'{baseUrl}{day}-{month}-2021'
      response = requests.get(url, headers=headers)

      if not response.status_code == 200:
        raise RuntimeError("Error fetching data from Cowin API")

      for resp in response.json()['sessions']:
        if resp['min_age_limit'] == 18 and resp['available_capacity'] > 0:
          pync.notify(f"Stock available in {resp['address']}, vaccine: {resp['slots']}")
        else:
          print(f"No vaccine slot for {day}, {month}, in {resp['address']}")

      if day >= 30:
        day = 1


# schedule.every(10).seconds.do(job)
schedule.every(10).minutes.do(job)


# Comment this if u don;t wnant to run this as deamon.
# fpid=os.fork()

# if fpid != 0:
#   sys.exit(0)


while 1:
  schedule.run_pending()
  # time.sleep(5)

# job()