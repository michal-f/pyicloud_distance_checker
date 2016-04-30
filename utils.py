#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import time


def log(*args):
    if settings.DEBUG_CONSOLE_LOGS is True:
        print('commands received: %s' % (
            ', '.join(['%s' % et for et in args]),
        ))


# Print iterations progress
def printProgress(iteration, total, prefix='', suffix='', decimals=2, barLength=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterations  - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength = int(round(barLength * iteration / float(total)))
    percents = round(100.00 * (iteration / float(total)), decimals)
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")

def sleeper():
    while True:
        # Get user input
        num = input('How long to wait: ')

        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue

        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())


def timecounter(interval):
    for i in range(0, interval):
        printProgress(i, interval, prefix='', suffix='', decimals=2, barLength=100)
        time.sleep(1)
        # print "time over RESTART"
        # timecounter(interval)
