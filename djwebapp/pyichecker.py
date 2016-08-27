#!/usr/bin/env python
# -*- coding: utf8 -*-
# __author__ = 'M.Frackowiak'
# OPENSOURCE PROJECT :)
"""
DISTANCE CHECKER BETWEEN DEVICE AND SELECTED POINT via ICLOUD SERVICE
outputs console logs and sound notifications about iCloud device movement.
"""
from __future__ import absolute_import
import time
import datetime
import utils
import os
# import sound_processor
from _exceptions.exceptions import *
from pyicloud import PyiCloudService
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.distance import great_circle
from utils import log
# from settings import *
from tools.credentials_handler import CredentialInput
LOGIN_DATA = {
    'login': '',
    'pass': ''
}
DEBUGGING = False
SOURCE_LOCATION_CORDINANTES = {
    'latitude': 54.503501,
    'longitude': 18.542396
}


def load_login_data():
    logincredentials = os.path.abspath(os.path.join(os.path.dirname(__file__), 'login_credentials.txt'))
    # check if credential file exists, if no then get credentials
    if not os.path.isfile(logincredentials):
        print("NO CREDENTIAL FILE FOUND!")
        credentialInput=CredentialInput()
        credentialInput.get()
    fo = open(logincredentials, 'r').read().split(":")
    LOGIN_DATA['login'] = fo[0]
    LOGIN_DATA['pass'] = fo[1]
    # fo = open('login', 'r').read().split(":")
    # LOGIN_DATA['login'] =
    # LOGIN_DATA['pass']
    print("LOADED ICLOUD PROFILE: ", LOGIN_DATA['login'], ":", LOGIN_DATA['pass'])


def temp_location():
    return {
        'timeStamp': '1456687186509L',
        'locationFinished': True,
        'longitude': 18.5679437779063,
        'positionType': u'GPS',
        'locationType': None,
        'latitude': 54.4446849078447,
        'isOld': False,
        'isInaccurate': False,
        'horizontalAccuracy': 50.0
    }


def temp_status():
    return {
        'deviceDisplayName': u'iPhone 6',
        'deviceStatus': u'201',
        'batteryLevel': 0.76,
        'name': u'Tamcia '
    }


def distance_handler(location_obj):
    log("[[DISTAMCE HANDLER START]]")
    geolocator = Nominatim()
    input_data = str(location_obj['latitude']) + ", " + str(location_obj['longitude'])
    log("[Input location str:" + input_data)
    location = geolocator.reverse(input_data)
    adres = location.address
    try:
        log("LOCATION ADRESS:" + adres)
    except Exception:
        try:
            log("LOCATION ADRESS:" + adres.encode("utf8"))
        except:
            pass
    # log("\nLOCATION RAW:"+location.address)
    POINT_A = (SOURCE_LOCATION_CORDINANTES['latitude'], SOURCE_LOCATION_CORDINANTES['longitude'])
    POINT_B = (location_obj['latitude'], location_obj['longitude'])

    vincentkm = (vincenty(POINT_A, POINT_B).kilometers)
    circlekm = (great_circle(POINT_A, POINT_B).kilometers)
    log("VINCENT KM:" + str(vincentkm))
    log("CIRCLE KM:")
    log(circlekm)

    vincent = (vincenty(POINT_A, POINT_B).meters)
    circle = (great_circle(POINT_A, POINT_B).meters)
    log("\nVINCENT meters:" + str(vincent))
    log("CIRCLE meters:")
    log(circle)
    log("[[DISTAMCE HANDLER END BEFORE RETURN]]")
    return {
        'vincent': vincent,
        'circle': circle,
        'adres': adres
    }

def get_location():
    load_login_data()
    api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])
    print("LOGIND DATA LOADED. TRY TO CONNECT")
    try:
        location = api.iphone.location()
        if len(location) > 0:
            print("[LOCATION OBJECT SUCCESSFULLY RECEIVED FROM ICLOUD API!]")
            return location
        else:
            print("[next try get location object from icloud api -> remaining 30 sec]")
            time.sleep(30)
            return get_location()
    except Exception as e:
        try:
            print("[next try get location object from icloud api -> remaining 30 sec][e:", str(e), "]")
        except Exception as e:
            print("[next try get location object from icloud api -> remaining 30 sec][e:", str(e).encode("utf8"), "]")
        time.sleep(30)
        return get_location()



def get_current():
    output=distance_handler(get_location())
    distance = str(output['vincent'])[:str(output['vincent']).find(".")]
    adres=output['adres']
    print("---------")
    print("adres:")
    print(adres.encode('utf8'))
    print ("distance:")
    print(distance)
    ouput_distance_object={
        "distance":distance,
        "adres":adres
    }
    return ouput_distance_object


if __name__ == '__main__':
    print("GET CURRENT LOCATION")
    get_current()



