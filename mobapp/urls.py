from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('sms/webhook', views.sms_registration),
]
