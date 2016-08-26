# Create your models here.
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
from djwebapp import settings
# from eventtools.models import BaseEvent, BaseOccurrence

MY_AVAILABILITY = (('1', _('Monday')),
                   ('2', _('Tuesday')),
                   ('3', _('Wednesday')),
                   ('4', _('Thursday')),
                   ('5', _('Friday')),
                   ('6', _('Saturday')),
                   ('7', _('Sunday')))


class CustomUserManager(BaseUserManager):
    def create_user(self, login, email, password=None):
        user = self.model(
            login=login,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password):
        user = self.create_user(login, email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    login = models.CharField(verbose_name=_('Login'), max_length=32, unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=32, blank=False, null=False)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=32, blank=False, null=False)
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=15, blank=True, null=True)
    days = MultiSelectField(choices=MY_AVAILABILITY, default=['1', '2', '3', '4', '5'])
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def get_column_name(self):
        return self.first_name + ' ' + self.last_name[:1] + '.'

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def user_creation(self, login, firstname, lastname, email, password, adminuser):
        CustomUser.objects.create(login=login,
                                  first_name=firstname,
                                  last_name=lastname,
                                  email=email,
                                  password=password,
                                  is_superuser=adminuser)



class EventType(models.Model):
    '''
    Simple ``Event`` classifcation.
    '''
    COLORS_CHOICES = (
        ('RED', 'red'),
        ('BLUE', 'blue'),
        ('ORANGE','orange'),
        ('GREEN','green'),
        ('YELLOW', 'yellow'),
        ('WHITE', 'white'),
    )

    label = models.CharField(_('label'), max_length=150, unique=True)
    fa_icon = models.CharField(_('fontawsome icon'), max_length=150, blank=True, null=True)
    color = models.CharField(_('color'),max_length=13, choices=COLORS_CHOICES, default='RED')
    for_all_users = models.BooleanField(default=False)

    #===========================================================================
    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.label


class Entry(models.Model):
    ACCEPTANCE_STATUS = (
        ("0", "not_decided"),
        ("1", "Accepted"),
        ("2", "Rejected")
    )
    AVAILABILITY_CHOICES = (
        ('NOT_AVAILABLE', 'not available'),
        ('AVAILABLE', 'available'),
        ('REMOTE', 'remote'),
        ('DAY_OFF', 'day_off'),
    )
    type = models.ForeignKey(EventType)
    title = models.CharField(_('title'),max_length=50, blank=True, null=True)
    body = models.TextField(_('body'),max_length=1000, blank=True, null=True)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(CustomUser, blank=True, null=True, related_name="Creator", verbose_name=_('creator'),)
    status= models.CharField(_('status'),max_length=13, choices=AVAILABILITY_CHOICES, default='NOT_AVAILABLE')
    admin_comment = models.TextField(_('admin comment'),max_length=1000, blank=True, null=True)
    accepted = models.CharField(_('accepted'),max_length=1, choices=ACCEPTANCE_STATUS, default="0")
    decision_by = models.ForeignKey(CustomUser, blank=True, null=True, related_name="Decision", verbose_name=_('decision by'),)

    def __unicode__(self):
        return unicode(self.creator)

    class Meta:
        verbose_name_plural = _('entries'),


class Note(models.Model):
    body = models.TextField(_('body'),max_length=1000, blank=True, null=True)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    note_author = models.ForeignKey(CustomUser, blank=True, null=True, related_name="note_author", verbose_name=_('note_author'),)
    comment = models.TextField(_('comment'),max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.creator)

    class Meta:
        verbose_name_plural = _('notes'),


class LanguageSetting(models.Model):
    LANGUAGES = (
        ('pl', 'Polish'),
        ('en', 'English'),
        ('de', 'German'),)

    customuser = models.ForeignKey(CustomUser)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='pl')


class ThemeSetting(models.Model):
    THEMES = (
        ('1', 'normal'),
        ('2', 'dark'),)

    customuser = models.ForeignKey(CustomUser)
    theme = models.CharField(max_length=1, choices=THEMES, default='1')

#     @property
#     def occurrence_data(self):
#         return {
#             'event_title': self.event.title,
#             'event_type': self.event_type.type,
#             'occurenece_title': self.occurenece_title,
#         }
#

class Post(models.Model):
    author = models.ForeignKey(CustomUser, blank=True, null=True, related_name="author")
    text = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [_('created')]

    def __unicode__(self):
        return self.text + ' - ' + self.author.username


class HTMLStorage(models.Model):
    storage=models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.storage


# #Swingtime ocurrence creator-> source django-swingtime
# from datetime import datetime
#
# def create_event(
#     title,
#     event_type,
#     description='',
#     start_time=None,
#     end_time=None,
#     note=None,
#     **rrule_params
# ):
#     '''
#     Convenience function to create an ``Event``, optionally create an
#     ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
#     rules match those for ``Event.add_occurrences``.
#
#     Returns the newly created ``Event`` instance.
#
#     Parameters
#
#     ``event_type``
#         can be either an ``EventType`` object or 2-tuple of ``(abbreviation,label)``,
#         from which an ``EventType`` is either created or retrieved.
#
#     ``start_time``
#         will default to the current hour if ``None``
#
#     ``end_time``
#         will default to ``start_time`` plus settings.DEFAULT_OCCURRENCE_DURATION
#         hour if ``None``
#
#     ``freq``, ``count``, ``rrule_params``
#         follow the ``dateutils`` API (see http://labix.org/python-dateutil)
#
#     '''
#
#     if isinstance(event_type, tuple):
#         event_type, created = EventType.objects.get_or_create(
#            fa_icon=event_type[0],
#             label=event_type[1]
#
#         )
#
#     event = Entry.objects.create(
#         title=title,
#         description=description,
#         event_type=event_type
#     )
#
#     if note is not None:
#         event.notes.create(note=note)
#
#     start_time = start or datetime.now().replace(
#         minute=0,
#         second=0,
#         microsecond=0
#     )
#
#     end = end or (start + settings.DEFAULT_OCCURRENCE_DURATION)
#     event.add_occurrences(start, end, **rrule_params)
#     return event