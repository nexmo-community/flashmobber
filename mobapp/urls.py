from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventList.as_view(), name='event-list'),
    path('logged-out', views.LoggedOut.as_view()),
    path('sms/webhook', views.sms_registration, name='registration-webhook'),
    path('event/create', views.CreateEvent.as_view(), name='event-create'),
    path('events/<slug:slug>', views.EventDetail.as_view(), name='event-detail'),
    path('events/<slug:slug>/edit', views.UpdateEvent.as_view(), name='event-edit'),
    path('events/<slug:slug>/billboard', views.EventBillboard.as_view(), name='event-billboard'),
    path('events/<slug:slug>/assign-number', views.AssignNumber.as_view(), name='number-assign'),
    path('events/<slug:slug>/list-numbers', views.ListOwnedNumbers.as_view(), name='number-assign-list'),
    path('events/<slug:slug>/broadcast', views.BroadcastView.as_view(), name='broadcast'),
    path('numbers/<str:country_code>/list', views.ListAvailableNumbers.as_view(), name='numbers-list'),
    path('number/buy', views.BuyNumber.as_view(), name='number-buy'),
    path('numbers/owned', views.ListOwnedNumbers.as_view(), name='numbers-owned'),
    path('numbers/search', views.SearchNumbers.as_view(), name='number-search'),
]
