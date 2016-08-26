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
import sound_processor
from _exceptions.exceptions import *
from pyicloud import PyiCloudService
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.distance import great_circle
from utils import log
from settings import *
from tools.credentials_handler import CredentialInput
LOGIN_DATA = {
    'login': '',
    'pass': ''
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


# def geoip():
#     """
#     ... after downloading the package, you need to import win_inet_pton in \Lib\site-packages\geoip.py and works like a charm.
#     :return:
#     """
#     print "===GEO IP==="
#     print geolite2.lookup_mine()
#     print "LOOKUP"
#     match = geolite2.lookup('46.186.86.99')
#     if match is not None:
#         print match.country
#         print match.continent
#         print match.timezone
#         print match.subdivisions
#         from geoip import open_database
#         with open_database('data/GeoLite2-City.mmdb') as db:
#             match = db.lookup_mine()
#             print 'My IP info:', match

# def run():
#     # load_login_data()
#     # api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])
#
#     if DEBUGGING is True:
#         devices_obj = json.loads(api.devices)
#         log("[api devices:]" + devices_obj)
#         iphone_obj = json.loads(api.iphone)
#         log("[iphone:]" + iphone_obj)
#         location = api.iphone.location()
#         status = api.iphone.status()
#         log("[status:]" + status)
#         log("[location:]" + location)
#         print "EXIT"
#
#     print "DISTANCE TEST"
#     distance_handler(temp_location())

FIRSTRUN = True

def runner():
    def get_location():
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

    def get_speed_level(difference):
        log("[GET SPEED LEVEL]")

        def out(level):
            log("[Speed level => " + str(level))
            return str(level)

        if difference < 18:
            return out(0)
        elif difference < 30:
            return out(1)
        elif difference < 45:
            return out(2)
        elif difference < 100:
            return out(3)
        elif difference < 200:
            return out(4)
        elif difference < 300:
            return out(5)
        else:
            return out(6)

    def get_distance_level(distance):
        log("[GET DISTANCE LEVEL]")
        dist = int(distance)

        def out(level):
            log("[Distance level => " + str(level))
            return str(level)

        if dist < 1000:
            return out(0)
        elif dist < 2000:
            return out(1)
        elif dist < 3000:
            return out(2)
        elif dist < 4000:
            return out(3)
        elif dist < 5000:
            return out(4)
        elif dist < 6000:
            return out(5)
        elif dist < 7000:
            return out(6)
        elif dist < 8000:
            return out(7)
        elif dist < 9000:
            return out(8)
        elif dist < 10000:
            return out(9)
        else:
            return out(10)

    def get_interval(difference, distance_input, interval=None):
        log("[GET_INTERVAL]in: ", 'diff:', str(difference), "  dist:", str(distance_input), "inter:", str(interval if interval is not None else "none"))
        distance=int(distance_input)

        def check_distance_is_valid_int(distance):
            try:
                int(distance)
                return True
            except Exception:
                return False

        if check_distance_is_valid_int(distance):
            try:
                if distance < 1100:
                    return 25
                elif distance > 7000:
                    return 90
                elif difference < 22:
                    return 60
                else:
                    return 40

            except Exception:
                log("[GET_INTERVAL][Exception!]returning default:[60,0]")
                return 60

        else:
            log("INTERVAL NO VALID INT RETURNING DEFAULT [60,0]")
            return 60

    def printer(counter, interval, difference, distance, adres=None):
        output = "\n[ " + str(counter) + " ][i:" + str(interval) + "][Diff: " + str(int(difference)) + " ][Dist: "
        output += str(distance)[:str(distance).find(".")] + "]"
        if adres is not None:
            output += "[Adres: " + adres + "]"
        try:
            print(output)
        except Exception:
            try:
                print(output.encode('utf8'))
            except Exception as printer_exception:
                log("[PRINTER EXCEPTION]:")
                print(printer_exception)

        try:
            fo = open("log.txt", "a")
            fo.write(str(datetime.datetime.now()) + "::::" + output)
            fo.close()
        except Exception as e:
            try:
                fo = open("log.txt", "a")
                fo.write(str(datetime.datetime.now()) + "::::" + output.encode("utf8") + "\n")
                fo.close()
            except Exception as printer_exception:
                log("[PRINTER EXCEPTION]:")
                print(printer_exception)

    def main_loop(current_location_obj):
        """
        PyICloud distance checker main interval loo
        :param current_location_obj:
        :return: icloud device location and moving information's via console log and sound play
        """

        interval, counter = 60, 0
        last_distance_obj = current_location_obj

        while True:
            counter += 1
            log("[MAIN LOOP][counter" + str(counter) + "]")

            # GET LOCATION OBJECT FROM ICLOUD
            log("[MAIN LOOP][API IPHONE]")
            location = api.iphone.location()

            # GET CURRENT DISTANCE FROM RECEIVED ICLOUD OBJECT
            log("[MAIN LOOP][CURRENT DISTANCE]")
            curr_distance_obj = distance_handler(location)

            # CALCULATE DISTANCE DIFFERENCE
            difference = abs(curr_distance_obj['vincent'] - last_distance_obj['vincent'])
            log("[MAIN LOOP][DIFFERENCE:" + str(difference) + "]")

            try:  # GET DISTANCE LEVEL
                distance = str(curr_distance_obj['vincent'])[:str(curr_distance_obj['vincent']).find(".")]
                distance_level = get_distance_level(distance)
            except Exception as e:
                print("[DISTANCE ERROR EXCEPTION]")
                distance_level, distance = "0", "0"

                print(e.message)

            try:  # GET SPEED LEVEL
                speed_level = get_speed_level(difference)
            except Exception as e:
                print("[SPEED CALCULATION ERROR EXCEPTION]")
                speed_level = "0"
                print(e.message)

            # CHECK INTERVAL
            log("[MAIN LOOP][INTERVAL]")
            try:
                interval = get_interval(difference, distance, interval)

            except Exception:
                raise IntervalException("raise_INTERVAL_exception")

            try:  # PRINT CONSOLE OUTPUT
                printer(counter, interval, difference, curr_distance_obj['vincent'], curr_distance_obj['adres'])
            except Exception as e:
                print("[PRINTER ERROR EXCEPTION]")
                print(e.message)

            try:  # PLAY SOUND INFO
                sound_processor.play(distance_level, "distance")
                time.sleep(1)
                sound_processor.play(speed_level, "speed")
            except Exception as e:
                print("[SOUND PLAYER ERROR EXCEPTION]")
                print(e.message)


            utils.timecounter(interval)
            last_distance_obj = curr_distance_obj

    # LOOP STARTER
    load_login_data()
    api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])

    print("[STARTING MAIN LOOP]")
    try:
        # print "start try main loop"
        # aa=distance_handler(get_location())
        main_loop(distance_handler(get_location()))
    except Exception as e:
        print("FAILED MAIN LOOP STARTING E:")
        raise e


# run()
# geoip()
runner()
