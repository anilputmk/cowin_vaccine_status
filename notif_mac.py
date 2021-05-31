import pync
# https://pypi.org/project/pync/
import schedule
# https://pypi.org/project/schedule/
import time
import os, sys
from daemonize import Daemonize
from datetime import datetime
# import notify2

import requests


baseUrl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=288&date='
pin_base_url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?'

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


def fetch_from_pin_code(pin_code, date, headers):
  url = f'{pin_base_url}pincode={pin_code}&date={date}'
  print(f"Polling pin code url: {url}")
  response = requests.get(url, headers=headers)
  if not response.status_code == 200:
      print(f"invalid response from server {response.status_code}")
      return
    
  if 'centers' not in response.json():
    print(f"Empty response from server: {date}, url: {url}")
    return

  for center in response.json()['centers']:
      print(f"Checking vaccine for address {center['address']}")
      for session in center['sessions']:
        if session['min_age_limit'] == 18 and session['available_capacity'] >0 :
          pync.notify(f"Stock available date={date}, in block: {center['block_name']}, address={center['address']}, available: {session['available_capacity']}")
          print(f"Stock available date={date}, in block: {center['block_name']}, addr= {center['address']}, available: {session['available_capacity']}")

  print('*******************************************************************')


def fetch_from_district_code(date, headers):
  url = f'{baseUrl}{date}'
  response = requests.get(url, headers=headers)

  if not response.status_code == 200:
    raise RuntimeError("Error fetching district data from Cowin API")

  for resp in response.json()['sessions']:
    if resp['min_age_limit'] == 18 and resp['available_capacity'] > 0:
      pync.notify(f"Stock available date={date}, in block: {resp['block_name']}, address={resp['address']}, available: {resp['available_capacity']}")
      print(f"Stock available date={date}, in block: {resp['block_name']}, addr= {resp['address']}, available: {resp['available_capacity']}")
      break

  print('*******************************************************************')


def job():
    # print("Running job")
    # pync.notify('Hello World')
    month=6
    day=1
    tumkur_pin_code=572101
    kyat_pin_code=572104
    tum_pin_code=572102
    sit_pin_code=572103
    print(f"Staring to poll {str(datetime.now())}")
    print(f"Day = {day}, month={month}")
    
  
    headers={
      'Accept-Language': 'hi_IN',
      'accept': 'application/json',
      'Host': 'cdn-api.co-vin.in',
      'User-Agent':'PostmanRuntime/7.26.8'
    }

    while True:
      print('*******************************************************************')
      print(f"Polling district url for day {day}")
      date = f'{day}-{month}-2021'
      fetch_from_district_code(date, headers)

      fetch_from_pin_code(tumkur_pin_code, date, headers)

      fetch_from_pin_code(kyat_pin_code, date, headers)

      fetch_from_pin_code(tum_pin_code, date, headers)

      fetch_from_pin_code(sit_pin_code, date, headers)
      
      day += 1
      if day > 31:
        break


schedule.every(10).seconds.do(job)
# schedule.every(10).minutes.do(job)


# Comment this if u don;t wnant to run this as deamon.
# fpid=os.fork()

# if fpid != 0:
#   sys.exit(0)


while 1:
  schedule.run_pending()
  # time.sleep(5)

# job()