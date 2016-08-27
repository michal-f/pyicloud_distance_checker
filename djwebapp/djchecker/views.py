# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic import View
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
import json
import urllib
import time

from pyichecker import *
import djchecker


def hello(request):
    return HttpResponse('Hello World!')

def home(request):
    return render_to_response('front.html', {'variable': 'world'})

class FrontView(View):
    template_name = 'front.html'
    products, catid = None, '0'

    def dispatch(self, request=None, *args, **kwargs):
        return render_to_response('front.html',{'variable': 'XXX'})

class LocationView(View):
    template_name = 'location.html'
    products, catid = None, '0'

    def dispatch(self, request=None, *args, **kwargs):
        response=get_current()
        distance=response['distance']
        adres=response['adres']
        location="[D:"+distance+"],[A:"+adres+"]"
        return render_to_response('location.html',{'location': location })

# ############### [ AJAX VIEWS ] ###################
class AjaxView(generic.View):
    """
    Ajax POST Requests Handler - Dynamic Content Edition Functionality.
    """
    # print("AJAXVIEWS")

    def post(self, request, **kwargs):
        # print("post")
        print "\n", 80 * "=", "\n", '>>> IN >>>', 'Ajax', 'Post: ', urllib.unquote_plus(
            self.request._body).decode(
            "utf-8"), "\n", 80 * "="
        ajax_request = urllib.unquote_plus(self.request._body).decode("utf-8").split("&")

        for i in ajax_request:
            print i

        # print("PYICHECKER!!!!!!!!")
        response=get_current()
        data = {'data':response}
        responsx = json.dumps(data)
        return HttpResponse(responsx)

ajax_view = AjaxView.as_view()
