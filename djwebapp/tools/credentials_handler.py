#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Credentials input handler class
"""
import os
import sys

# from xml.etree.ElementTree import ElementTree
# from collections import OrderedDict
#
# from django.core.exceptions import ObjectDoesNotExist
# from django.template.defaultfilters import slugify
# from django.core.management.base import BaseCommand
# from django.conf import settings
# from django.core.cache import cache


# DJANGOOOOOOOOOOOOOOOOOOOOOOOO
# class CredentialInput():
#     """
#     [Get icloud credentials from user input -> save to file]
#     """
#
#     def __init__(self, *args, **kwargs):
#         # super(Command, self).__init__(*args, **kwargs)
#         # self.help = self.style.WARNING("\n" + 70 * "_" + "\n [Product importer for provided XML file's] help info:\n\n")
#         # self.help += self.style.MIGRATE_HEADING("A XML File can be passed:\n") + " * via -f option : python manage.py import -f path\XMLfile.xml\n"
#         # self.help += " * placed in default import folder: " + self.style.MIGRATE_HEADING("'...project_root/XML/' ")
#         # self.help += "\n\n   if XML_path is not passed via -f then searching in:\n   default folder ->"
#         # self.help += self.style.MIGRATE_HEADING(" ...project_root/XML/ ")
#         # self.help += self.style.WARNING("\n" + 70 * "_")
#
#     def add_arguments(self, parser):
#         parser.add_argument('-f', dest='filepath', nargs='+', type=str)
#
#     def handle(self, *args, **options):
#         """
#         ['import' command handler]
#         possible params:
#          * '-f file_path'
#         """
#         self.stdout.write('\n [Django Management Command] ' + self.style.SUCCESS('starting: product import'))
#         x, c, input = XMLparser(), XMLcount(), []
#         try:
#             if options['filepath'] is not None:
#                 self.stdout.write(self.style.SUCCESS('-> found XML filepath param: ' + str(options['filepath'])))
#                 input.append(options['filepath'][0])
#             else:
#                 for filepath in x.check_input_dir():
#                     input.append(
#                         os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'XML', filepath)))
#             if len(input) > 0:
#                 self.stdout.write(self.style.SUCCESS('-> counting XML input ... '))
#                 products_to_import = c.countXML(input)
#                 self.stdout.write(self.style.SUCCESS('-> found ' + str(products_to_import) + ' products. import started: '))
#                 for filepath in input:
#                     x.parseXML(filepath, products_to_import)
#
#                 self.stdout.write(self.style.SUCCESS('-> XML product import finished!'))
#             else:
#                 self.stdout.write(self.style.ERROR('-> Import failed! No XML files found...'))
#         except Exception as e:
#             if str(e).find('Error 3]') > 0:
#                 self.stdout.write(self.style.ERROR("\nException: XML input not found!" + self.help))
#             else:
#                 self.stdout.write(self.style.ERROR("\nException:" + str(e) + "\n\n info ->" + self.help))
#     def start(self):
#
#


class CredentialInput():
    """
    [Get icloud credentials from user input -> save to file]
    """

    def __init__(self, *args, **kwargs):
        print("ICloud credential handler!")

    def get(self):
        print("GET CREDENTIALS")
        username = raw_input('Enter iCloud username (tracked idevice):')
        password = raw_input('Enter iCloud password:')
        credentials = username + ":" + password
        credential_file_name = "login_credentials.txt"
        print("Your credentials data are: " + credentials + " => creating file => "+credential_file_name)
        credential_file= open(credential_file_name,"w")
        credential_file.write(credentials)
        credential_file.close()
        print("login credentials successfully saved!")


if __name__ == '__main__':
    get_input = CredentialInput()
    get_input.get()
