from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from nexmodj.decorators import sms_webhook

@login_required
def index(request):
    return render(request, "mobapp/index.html")


@sms_webhook(validate_signature=False)
def sms_registration(request):
    print(f"Got a text from {request.sms.msisdn} saying {request.sms.text!r}")
    return HttpResponse("What do you call this?")
