#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys

from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand
# from django.utils.translation import ugettext_lazy as _

# from cal.models import *
from djchecker.models import *
from django.conf import settings
# from django.core.cache import cache

# from cal.utils import log
# os.chdir("../")
# sys.path.append(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


# def setUp(self):
#     admin = CustomUser.objects.create_superuser("admin", email="admin@user.pl", password="admin")
#     CustomUser.objects.create(
#         login=unicode("User"),
#         first_name=unicode("FirstName"),
#         last_name=unicode("LastName"),
#         email=unicode("user@email.com"),
#         days=['1', '3', '5'],
#         password=unicode("password")
#     )
def log(input):
    if True:
        print(input)


class InitDataCreate:
    """ Create and save initial event types """

    def __init__(self, *args, **kwargs):
        # CustomUser.objects.create_superuser("admin", email="admin@user.pl", password="admin")
        log("[class InitDataCreate][init]:starting init data creator class")


    def create_admin(self):
        log(">@>[StartCommand][init Admin in DB]")
        admin = CustomUser.objects.create_superuser("admin3", email="admin3@user.pl", password="Mf12121212")

    def demo(self, login):
        log(">@>[class InitDataCreate][demo]creating demo user")
        CustomUser.objects.create(
            login=unicode("User_"+login),
            first_name=unicode("FirstName"),
            last_name=unicode("LastName"),
            email=unicode(login+"user@email.com"),
            days=['1', '2', '3', '5'],
            password=unicode("pass"),
            is_superuser=False
        )


    def init_data(self):
        log(">@>[class InitDataCreate][def init_data]creating initial data")
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("late start"), for_all_users=False, fa_icon="fa-level-down", color="orange")
        # except ObjectDoesNotExist:
        #     pass
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("earlier quit"), for_all_users=False, fa_icon="fa-level-down", color="orange")
        # except ObjectDoesNotExist:
        #     pass
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("single day event"), for_all_users=False, fa_icon="fa-long-arrow-down", color="orange")
        # except ObjectDoesNotExist:
        #     pass
        #
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("range event"), for_all_users=False, fa_icon="fa-arrows-h", color="orange")
        # except ObjectDoesNotExist:
        #     pass
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("other work time event"), for_all_users=True, fa_icon="fa-thumb-tack", color="orange")
        # except ObjectDoesNotExist:
        #     pass
        # try:
        #     td, created = EventType.objects.get_or_create(label=_("public event for all users"), for_all_users=False, fa_icon="fa-users", color="green")
        # except ObjectDoesNotExist:
        #     pass
        log(">@>[class InitDataCreate][def init_data]initial data successfully created!")
        return True

class Command(BaseCommand):
    """
    [Management Command -> Generate initial data products from XML]
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.help = self.style.WARNING("\n" + 70 * "_" + "\n [Initial data creator]\n\n")
        self.help += self.style.WARNING("\n" + 70 * "_")
        # log(">@>[0.)Run init data creator]")
        log("-> Run Management Command: 'start' - class init")
        self.init_creator=InitDataCreate()
        # log(">@>[1.)After-> Run init data creator]")



    def add_arguments(self, parser):
        parser.add_argument('-i', dest='info', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        ['import' init data handler]
        possible params:
         * '-i demo'
        """
        self.stdout.write('---------------------------------------------------\n [Django Management Command] ' + self.style.SUCCESS('starting: init data import'))
        log("---------------------------------------------------")
        # log("OPTIONS COUNT:"+str(len(options)))
        # for i in options:
        #     log("  "+i)
        try:
            if options['info'] is not None:

                print("-> PASSED ARGUMENTS -i: ...")
                print(options['info'])

                if options['info'][0] == 'demo':
                    log("init start! -> creating calendar with demo data!")
                    self.stdout.write(self.style.SUCCESS('-> preparing new calendar with demo data,' + str(options['info'])))
                    for i in range(1,10):
                        self.init_creator.demo(str(i))
                    self.style.SUCCESS("init complete! -> calendar with demo data!")

                #COMMAND=> python manage.py start -i admin
                elif options['info'][0] == 'admin':
                    self.init_creator.create_admin()
                    self.style.SUCCESS("admin user created!")
                else:
                    self.style.SUCCESS("no option recoginized log pased option for command")
                    try:
                        log(str(options['info']))
                    except Exception as e:
                        print e
                    log("")


            else:
                #
                log("init start! -> NO ARGUMENTS PASSED")
                log("START DEFAULT IMPORT PROCCEDURE FOR COMMAND 'START' with no arguments")
                # self.stdout.write(self.style.SUCCESS('-> creating new calendar!'))
                # self.init_creator.init_data()
                # self.style.SUCCESS("init complete! -> created new calendar")

        except Exception as e:
            self.stdout.write(self.style.ERROR("\nException: (init data creator) :" + str(e)+ self.help))
