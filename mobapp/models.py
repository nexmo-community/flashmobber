from datetime import datetime

from django.db import models
from django.urls import reverse

import phonenumbers

def this_year():
    return datetime.now().year


class Event(models.Model):
    class Meta:
        ordering = ['-year', 'name']

    name = models.CharField(max_length=255)
    year = models.IntegerField(
        default=this_year
    )
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name} ({self.year})'

    def __repr__(self):
        return f'<Event {self.name} ({self.year})>'

    
class OwnedNumber(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='numbers', null=True)
    msisdn = models.CharField(max_length=32, unique=True)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.msisdn} ({self.country_code})'
    
    def __repr__(self):
        return f'<OwnedNumber {self.msisdn} ({self.country_code})>'

    def formatted_msisdn(self):
        return phonenumbers.format_number(phonenumbers.parse('+' + self.msisdn), phonenumbers.PhoneNumberFormat.INTERNATIONAL)


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=255)
    msisdn = models.CharField(max_length=32, db_index=True)

    def __str__(self):
        return f"{self.msisdn} registered for {self.event.name}"

    class Meta:
        unique_together = ['event', 'msisdn']