#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import time
import os

from xml.etree.ElementTree import ElementTree
from collections import OrderedDict

from django.core.cache import cache


# os.chdir("../")
sys.path.append(os.path.dirname(__file__))
import settings

#
# def get_time():
#     ts = time.time()
#     return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#
#
# def get_time_name():
#     ts = time.time()
#     return datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
#
#

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




















#
# # -*- coding: utf-8 -*-
# import os
# import time
# import datetime
# from settings import *
#

# def log(*args):
#     if DEBUG_CONSOLE_LOGS is True:
#         try:
#             print('[debug log]: %s' % (
#                 ', '.join(['%s' % et for et in args]),
#             ))
#         except Exception:
#             pass
#
#
# def writer(path, data):
#     try:
#         with open(path, "a+") as f:
#             f.write(data+ "\n")
#     except Exception:
#         try:
#             with open(path, "a+") as f:
#                 f.write(data.encode("utf8")+ "\n")
#         except Exception as e:
#             log(e)
#
#
# class OutputStore:
#     """
#     save requested pages
#     """
#     output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
#
#     def __init__(self, *args, **kwargs):
#         self.profile_links = os.path.abspath(os.path.join(self.output_folder, 'profile_links.txt'))
#         self.scraped_urls = os.path.abspath(os.path.join(self.output_folder, 'scraped_urls.txt'))
#         self.log_file = os.path.abspath(os.path.join(self.output_folder, 'logs.txt'))
#         if os.path.isdir(self.output_folder) is False:
#             os.mkdir(self.output_folder)
#
#     def save_profile_links(self, link_list):
#         if SAVE_PROFILE_LINKS:
#             for link in link_list:
#                 writer(self.profile_links, link)
#
#     def save_scraped_url(self, url):
#         if SAVE_VISITED:
#             writer(self.scraped_urls, url)
#
#     def save_log(self, data=None):
#         if SAVE_LOGS:
#             log_data="["+get_time()+"]:"+data if data is not None else "empty_log"
#             writer(self.log_file, log_data)
#
#     def savehtml(self, response_data):
#         """
#         save visited pages HTML -> with status code = 200
#         """
#         if SAVE_VISITED_PAGES:
#             html_output_dir = os.path.abspath(os.path.join(self.output_folder, 'html'))
#             if os.path.isdir(html_output_dir) is False:
#                 os.mkdir(html_output_dir)
#
#             store_file_name = get_time_name() + ".html"
#             writer(os.path.abspath(os.path.join(html_output_dir, store_file_name)), response_data)
#
#     def save_exception(self, response_data):
#         """
#         save exception response data with status code !=200
#         """
#         if SAVE_REQUEST_EXCEPTIONS_OUTPUT:
#             exception_output_dir = os.path.abspath(os.path.join(self.output_folder, 'failed'))
#             if os.path.isdir(exception_output_dir) is False:
#                 os.mkdir(exception_output_dir)
#
#             response_headers=response_data.status_code
#             response_json=response_data.json()
#             response_str = ''.join(response_data.text)
#
#             store_file_name=get_time_name()
#
#             header_filename = os.path.abspath(os.path.join(exception_output_dir, store_file_name+'.headers'))
#             json_filename = os.path.abspath(os.path.join(exception_output_dir, store_file_name+'.json'))
#             response_filename = os.path.abspath(os.path.join(exception_output_dir, store_file_name+'.response'))
#
#             writer(header_filename, response_headers)
#             writer(json_filename, response_json)
#             writer(response_filename, response_str)