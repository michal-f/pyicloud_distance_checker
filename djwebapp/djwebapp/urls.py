# -*- coding: utf-8 -*-
"""djwebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from djchecker import views


def javascript_settings():
    js_conf = {'ajax_view': reverse('ajax-view')}
    return js_conf


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.FrontView.as_view()),
    url(r'^hello/', 'djchecker.views.hello'),
    url(r'^home/', 'djchecker.views.home'),
    url(r'^l/', views.LocationView.as_view()),
    url(r'^ajax/$', views.ajax_view, name='ajax-view'),
]
