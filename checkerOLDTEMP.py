#!/usr/bin/env python
# -*- coding: utf8 -*-
# __author__ = 'M.Frackowiak'
"""
DISTANCE CHECKER BETWEEN DEVICE AND SELECTED POINT via ICLOUD SERVICE

DO ZAIMPLEMTOWANIA
-https://pypi.python.org/pypi/geolocation-python/0.2.2

"""
from __future__ import absolute_import
import time
import os
from _exceptions.exceptions import *
from pyicloud import PyiCloudService
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.distance import great_circle
import mp3play

CONSOLE_LOG = True
DEBUGGING = True
SYRKOMLI = {
    'latitude': 54.503501,
    'longitude': 18.542396
}


def log(text):
    if CONSOLE_LOG is True:
        print text


LOGIN_DATA = {
    'login': '',
    'pass': ''
}


def load_login_data():
    fo = open('login', 'r').read().split(":")
    LOGIN_DATA['login'] = fo[0]
    LOGIN_DATA['pass'] = fo[1]
    print "LOADED ICLOUD PROFILE: ", LOGIN_DATA['login'], ":", LOGIN_DATA['pass']


def temp_location():
    return {
        'timeStamp': 1456687186509L,
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
    geolocator = Nominatim()
    input_data = str(location_obj['latitude']) + ", " + str(location_obj['longitude'])
    log("[Input location str:" + input_data)
    location = geolocator.reverse(input_data)
    adres = location.address
    log("\nLOCATION ADRESS:" + adres)
    # log("\nLOCATION RAW:"+location.address)

    POINT_A = (SYRKOMLI['latitude'], SYRKOMLI['longitude'])
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
    return {
        'vincent': vincent,
        'circle': circle,
        'adres': adres
    }


#
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
#
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


def alarm(sound=None, type=None):
    THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    def get_speed_sound(level):
        speed_level_sound_obj = {
            0: '0_Blop-Mark_DiAngelo-79054334.mp3',
            1: '1_Cartoon Walking-SoundBible.com-2130722123.mp3',
            2: '2_Fast_Heel_Walk-Kyanna_Johnson-1646343608.mp3',
            3: '3_Galloping Horse-SoundBible.com-1411555122.mp3',
            4: '4_CarAcceleratingSoundBible.com-28596349.mp3',
            5: '5_Train_Approach_n_Pass-Mike_Koenig-678807208.mp3',
            6: '6_Healicopter_Approach-Mike_Koenig-1395051800.mp3',
        }
        sound_path = os.path.abspath(os.path.join(THIS_DIR, 'sounds', 'SPEED', speed_level_sound_obj[level]))
        return sound_path

    def get_speak_sound(level):
        spoken_sound_obj = {
            0: 'mniejniz2km.mp3',
            1: 'mniejniz4.mp3',
            2: 'objectsiezbliza.mp3',
            3: 'objectsiezblizaszybko.mp3',
            4: 'objektznajdujesiewodleglosc.mp3'
        }

        sound_path = os.path.abspath(os.path.join(THIS_DIR, 'sounds', 'SPEAK', spoken_sound_obj[level]))
        return sound_path

    def get_alarm_sound(level):
        alarm_sound_obj = {
            0: '0_Woosh-Mark_DiAngelo-4778593.mp3',
            1: '1_35752^CarAlarmSet.mp3',
            2: '2_91540^caralarm.mp3',
            3: '3_24483^pchick-alarm.mp3',
            4: '4_71766^alarm.mp3',
            5: '5_44216^alarm.mp3',
            6: '6_86502^alarm.mp3',
            7: '7_97744^ALARM.mp3'
        }

        sound_path = os.path.abspath(os.path.join(THIS_DIR, 'sounds', 'ALARMS', alarm_sound_obj[level]))
        return sound_path

    def player(filename):
        clip = mp3play.load(filename)
        clip.play()
        time.sleep(min(30, clip.seconds()))
        clip.stop()

    if type == "speed":
        log("speed alarm nr:" + str(sound))
        player(get_speed_sound(sound))
    elif type == "speak":
        log("speed alarm nr:" + str(sound))
        player(get_speak_sound(sound))
    else:
        log("alarm nr:" + str(sound))
        player(get_alarm_sound(sound))


def runner():
    def get_location():
        try:
            print "GET LOCATION"
            location = api.iphone.location()
            if len(location) > 0:
                print "[LOCATION OBJECT SUCCESSFULLY RECEIVED FROM ICLOUD API!]"
                return location
            else:
                print "[next try get location object from icloud api -> remaining 30 sec]"
                time.sleep(30)
                return get_location()
        except Exception as e:
            print "[next try get location object from icloud api -> remaining 30 sec][e:", str(e).encode("utf8"), "]"
            time.sleep(30)
            return get_location()

    def get_speed_level(difference):
        speed_level_obj = {
            0: "no_motion",
            1: "veryslow",
            2: "slow",
            3: "mid",
            4: "fast",
            5: "veryfast",
            6: "ultrafast"
        }

        def out(level):
            log("[Speed level => " + speed_level_obj[level])
            return level

        if difference < 20:
            return out(0)
        elif difference < 30:
            return out(1)
        elif difference < 40:
            return out(2)
        elif difference < 50:
            return out(3)
        elif difference < 70:
            return out(4)
        elif difference < 150:
            return out(5)
        else:
            return out(6)

    def get_interval(difference, curr_distance_obj, interval):

        last_interval = interval
        speed_level = get_speed_level(difference)
        base = 120

        if speed_level > 0:
            base_interval = base / speed_level
        else:
            base_interval = 180
        if int(curr_distance_obj['vincent']) < 1500:
            new_interval = [base_interval / 2, 0, speed_level]
        elif int(curr_distance_obj['vincent']) < 5000:
            new_interval = [base_interval, 1, speed_level]
        elif int(curr_distance_obj['vincent']) < 10000:
            new_interval = [base_interval * 2, 2, speed_level]
        elif int(curr_distance_obj['vincent']) < 20000:
            new_interval = [base_interval * 3, 3, speed_level]
        elif int(curr_distance_obj['vincent']) < 40000:
            new_interval = [base_interval * 4, 4, speed_level]
        elif int(curr_distance_obj['vincent']) < 60000:
            new_interval = [base_interval * 5, 5, speed_level]
        elif int(curr_distance_obj['vincent']) < 100000:
            new_interval = [base_interval * 10, 6, speed_level]
        else:
            new_interval = [60 * 60, 7]

        log("[Next check interval => " + str(new_interval) + "sec.]")
        return new_interval

    def printer(counter, interval, difference, distance, adres=None):
        output = "\n[ " + str(counter) + " ][i:" + str(interval) + "][Diff: " + str(int(difference)) + " ][Dist: "
        output += str(distance)[:str(distance).find(".")] + "]"
        if adres is not None:
            output += "[Adres: " + adres + "]"
        try:
            print output
        except Exception as e:
            print e
            raise

    def main_loop(current_location_obj):
        interval, counter = 60, 0
        last_distance_obj = current_location_obj

        while True:
            counter += 1
            location = api.iphone.location()
            curr_distance_obj = distance_handler(location)

            difference = abs(curr_distance_obj['vincent'] - last_distance_obj['vincent'])

            try:
                interval = get_interval(difference, curr_distance_obj, interval)[0]
                interval = 30
                interval_level = get_interval(difference, curr_distance_obj, interval)[1]
                speed_level = get_interval(difference, curr_distance_obj, interval)[2]
            except Exception:
                raise IntervalException("raise_INTERVAL_exception")

            try:
                alarm(speed_level, "speed")
                alarm(interval_level, "")
            except Exception:
                raise AlarmException("raise_ALARM_exception")

            try:
                printer(counter, interval, difference, curr_distance_obj['vincent'], curr_distance_obj['adres'])
            except Exception as e:
                print e.message
                # raise PrinterException("raise printer exception")

                # # OBJECT IS MOVING FAST!
                # if float(difference) > 100.0:
                #     print 20 * "---"
                #     print "\n\n" + 20 * "!X![difference>100!X!" + "\n\n"
                #     alarm(2)
                #
                # # OBJECT IS NOT MOVING
                # if float(difference) < 5.0:
                #     print "[", str(counter), "][R<1m][BEZ ZMIAN][ODLEGLOSC:", str(
                #         curr_distance_obj['vincent']), "difference:  ", str(
                #         difference), "  ]", "   >", curr_distance_obj['adres']
                #     alarm(1)
                # else:
                #     # OBJECT IS APPROACHING
                #     if curr_distance_obj['vincent'] < last_distance_obj['vincent']:
                #
                #         if float(difference) < 20.0:
                #             alarm(3)
                #             print "!PONAD 20 METROW!!!UWAGA[", str(
                #                 counter), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                #                 curr_distance_obj['vincent']), " [difference::::>  ", str(difference), "  ]   >", \
                #                 curr_distance_obj['adres'], "\n"
                #         elif float(difference) < 30.0:
                #             print "\n!!!!!!!!!!!!!! 20- 30 METROW)\nUWAGA[", str(
                #                 COUNTER), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                #                 curr_distance_obj['vincent']), " [difference::::>  ", str(difference), "  ]   >", \
                #                 curr_distance_obj['adres']
                #             alarm(0)
                #         else:
                #
                #             alarm(4)
                #             print "\n\n" + 500 * "!!!" + "\n\n"
                #             print "UWAGA PONAD 30M na minute[", str(
                #                 COUNTER), "][R>1m][OBJEKT SIE ZBLIZA!!!!],[ODLEGLOSC:", str(
                #                 curr_distance_obj['vincent']), " [difference::::>  ", str(difference), "  ]   >", \
                #                 curr_distance_obj['adres']

                #     # UNDER 2000 METER
                #     if curr_distance_obj['vincent'] < 2000:
                #         alarm(6)
                #         alarm(100, 0)
                #         print "\n MNIEJ NIZ 2 KM ZOSTALO!!!!\n"
                #
                # # OBJECT IS MOVING AWAY!
                # else:
                #     print "UWAGA[", str(counter), "][R>1m][OBJEKT SIE ODDALA!][ODLEGLOSC:", str(
                #         curr_distance_obj['vincent']), "  [difference:  ", str(difference), "  ]   >", \
                #         curr_distance_obj['adres']
                #     alarm(5)
            # print "INTERVAL:", str(interval)
            time.sleep(interval)
            last_distance_obj = curr_distance_obj

    # LOOP STARTER
    load_login_data()
    api = PyiCloudService(LOGIN_DATA['login'], LOGIN_DATA['pass'])

    print "[STARTING MAIN LOOP]"
    try:
        # print "start try main loop"
        # aa=distance_handler(get_location())
        main_loop(distance_handler(get_location()))
    except Exception as e:
        print "FAILED MAIN LOOP STARTING E:"
        raise e


# run()
# geoip()
runner()
