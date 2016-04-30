# https://github.com/downloads/AVbin/AVbin/AVbin10-win64.exe
# python alarmer.py 3

import winsound

import os
import sys
import time
import mp3play

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
THIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
SOUNDS = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), '24483^pchick-alarm.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '35752^CarAlarmSet.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '44216^alarm.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '71766^alarm.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '86502^alarm.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '91540^caralarm.mp3')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '97744^ALARM.mp3')),
]


def alarm(sound):
    SOUNDS_NAMES = [
        '24483^pchick-alarm.mp3',
        '35752^CarAlarmSet.mp3',
        '44216^alarm.mp3',
        '71766^alarm.mp3',
        '86502^alarm.mp3',
        '91540^caralarm.mp3',
        '97744^ALARM.mp3',
    ]

    filename = SOUNDS_NAMES[int(sound)]
    clip = mp3play.load(filename)
    clip.play()
    time.sleep(min(30, clip.seconds()))
    clip.stop()
    print "EXIT"


if __name__ == '__main__':
    # print "0"
    # alarm(0)
    print "1"
    alarm(1)
    # print "2"
    # alarm(2)
    print "3"
    alarm(3)
    # print "4"
    # alarm(4)
    print "5"
    alarm(5)
    # print "6"
    # alarm(6)
