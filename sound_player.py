#!/usr/bin/env python
# -*- coding: utf8 -*-
# __author__ = 'M.Frackowiak'
"""
DISTANCE CHECKER BETWEEN DEVICE AND SELECTED POINT via ICLOUD SERVICE

DO ZAIMPLEMTOWANIA
-https://pypi.python.org/pypi/geolocation-python/0.2.2

"""
from __future__ import absolute_import
import sys
import time
import numbers
import os
from _exceptions.exceptions import *

import mp3play

import subprocess
import multiprocessing
import json
import glob
import shutil
import threading
import time as imported_time
# from datetime import datetim
from utils import log
from settings import *


def alarm(sound=None, type=None):
    log("[ALARM][Start]input: sound->", sound if sound is not None else "NONE", " type->", type if type is not None else "NONE")
    THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    def clear_input(var):
        log("[ALARM][INPUT CLEANER]input:", var)
        try:
            if isinstance(var, numbers.Integral):
                log("[ALARM][INPUT CLEANER][RETURN INT]input:", var)
                return var
            else:
                temp = " " + var
                if temp.find(",") > 0:
                    return temp.replace(",", "").strip()
                else:
                    return temp.replace(",", "").strip()
        except Exception as e:
            print(InputCleaningException)
            raise(InputCleaningException(e))

    sound = clear_input(sound)
    type = clear_input(type)
    log("[ALARM][cleaned input]input: sound->", sound if sound is not None else "NONE", " type->", type if type is not None else "NONE")

    def get_speed_sound(level):
        speed_level_sound_obj = {
            0: '0_Blop-Mark_DiAngelo-79054334.mp3',
            1: '1_Cartoon Walking-SoundBible.com-2130722123.mp3',
            2: '2_Fast_Heel_Walk-Kyanna_Johnson-1646343608.mp3',
            3: '3_Galloping Horse-SoundBible.com-1411555122.mp3',
            4: '4_CarAcceleratingSoundBible.com-28596349.mp3',
            5: '5_Train_Approach_n_Pass-Mike_Koenig-678807208.mp3',
            6: '6_Healicopter_Approach-Mike_Koenig-1395051800.mp3',
            7: '6_Healicopter_Approach-Mike_Koenig-1395051800.mp3',
        }
        sound_path = os.path.abspath(os.path.join(THIS_DIR, 'sounds', 'SPEED', speed_level_sound_obj[level]))
        return sound_path

    def get_distance_sound(level):
        speed_level_sound_obj = {
            0: '0.mp3',
            1: '1.mp3',
            2: '2.mp3',
            3: '3.mp3',
            4: '4.mp3',
            5: '5.mp3',
            6: '6.mp3',
            7: '7.mp3',
            8: '8.mp3',
            9: '9.mp3',
            10: 'over10.mp3',
        }
        sound_path = os.path.abspath(os.path.join(THIS_DIR, 'sounds', 'KM', speed_level_sound_obj[level]))
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
    elif type == "distance":
        log("distance alarm nr:" + str(sound))
        player(get_distance_sound(sound))
    elif type == "speak":
        log("speed alarm nr:" + str(sound))
        player(get_speak_sound(sound))
    else:
        log("alarm nr:" + str(sound))
        player(get_alarm_sound(sound))


def player(level, type):
    print("[Player][LEVEL: "+level+", TYPE: "+ type+ "]")
    try:
        alarm(int(level), type)
    except Exception:
        raise AlarmException("raise_ALARM_exception")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        player(sys.argv[1], sys.argv[2])
    else:
        print("[Error-> 2 Parameters required -> level, sound_type]")

