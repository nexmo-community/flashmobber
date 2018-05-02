from django.shortcuts import render, HttpResponse, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from nexmodj.decorators import sms_webhook

from .models import Event, OwnedNumber, Registration

from nexmodj import client


@sms_webhook
def sms_registration(request):
    sms = request.sms
    print(f"Got a text from {request.sms.msisdn} saying {request.sms.text!r}")

    try:
        event = OwnedNumber.objects.get(msisdn=request.sms.to).event
        if event is None:
            print(f"Message received to a number not assigned to any event: {request.sms.to}")
            return HttpResponseForbidden("Cannot receive messages to unassigned numbers!")
    except OwnedNumber.DoesNotExist:
        print(f"Message received from unknown number (number not registered by FlashMobber): {request.sms.to}")
        return HttpResponseForbidden("Unknown Number!")

    # if 'leave': then remove 'msisdn' from assigned event.
    if sms.text.strip().lower() == 'leave':
        request.sms.reply(
            f"You've been removed from our {event.name} promotion! Sorry to see you go 🙁",
            'unicode',
        )
        event.registrations.get(msisdn=request.sms.msisdn).delete()
    else:
        try:
            registration = event.registrations.get(msisdn=request.sms.msisdn)
            # 'msisdn' already assigned to event: send instructions on how to leave.
            request.sms.reply(
                f"You're already registered for {event.name}! If you'd like to leave, send LEAVE to {request.sms.to}",
                'unicode',
            )
        except Registration.DoesNotExist:
            registration = Registration(event=event, msisdn=request.sms.msisdn, name=request.sms.text.strip())
            registration.save()
            request.sms.reply(
                f"You're registered for {event.name}! Standby for further details ...",
                'unicode',
            )
    return HttpResponse("Successful SMS processing.")


class LoggedOut(TemplateView):
    template_name = 'mobapp/logged_out.html'


class EventList(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'mobapp/index.html'


class EventDetail(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'mobapp/event_detail.html'


class CreateEvent(CreateView):
    model = Event
    fields = ['name', 'year', 'slug']


class UpdateEvent(UpdateView):
    model = Event
    fields = ['name', 'year', 'slug']


class DeleteEvent(DeleteView):
    model = Event


class ListAvailableNumbers(View, AccessMixin):
    def get(self, request, country_code):
        response = client.get_available_numbers(country_code, features='SMS')
        print(response)
        
        if response.get('numbers') is not None:
            return render(request, 'mobapp/numbers_available.html', dict(numbers=response['numbers'], country_code=country_code))
        else:
            raise Exception('Invalid object returned by get_available_numbers')


def quicky(request):
    request.build_absolute_uri(reverse('registration-webhook'))



class BuyNumber(View, AccessMixin):
    def post(self, request):
        country_code = request.POST['country_code']
        msisdn = request.POST['number']

        print(f"Buying {msisdn} in {country_code}")
        # buy number
        # response = client.buy_number(country=country_code, msisdn=msisdn)
        # if response['error-code'] != "200":
        #     raise Exception(f"There was an error ({response.get('error-code')}) buying the number: {response.get('error-code-label')}")
        OwnedNumber(msisdn=msisdn, country_code=country_code).save()
        # configure the number to point to our registration webhook
        webhook_uri = request.build_absolute_uri(reverse('registration-webhook'))
        # client.update_number({
        #    'country': country_code,
        #    'msisdn': msisdn,
        #    'moHttpUrl': webhook_uri,
        # })

        return HttpResponseRedirect(reverse('numbers-owned'))


class ListOwnedNumbers(View):
    model = OwnedNumber
    context_object_name = 'numbers'
    template_name = "mobapp/numbers_owned.html"

    def get(self, request, slug=None):
        print(f'getting, slug={slug!r}')
        numbers = OwnedNumber.objects.all()
        print(numbers)
        event = None
        if slug:
            event = Event.objects.get(slug=slug)
        return render(request, self.template_name, { 'numbers': numbers, 'event': event })


class AssignNumber(View, SingleObjectMixin):
    model = Event
    context_object_name = 'event'

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        owned_number = OwnedNumber.objects.get(msisdn=request.POST['number'])
        owned_number.event = event
        owned_number.save()

        return HttpResponseRedirect(reverse('number-assign-list', kwargs={'slug': event.slug}))


class EventBillboard(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'mobapp/event_billboard.html'