from django.shortcuts import render, HttpResponse

from .decorators import sms_webhook


@sms_webhook
def index(request):
    return HttpResponse("What do you call this?")