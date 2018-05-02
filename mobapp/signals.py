from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registration

import pusher

print("signals imported")

pusher_client = pusher.Pusher(
  app_id=getattr(settings, "PUSHER_APP_ID", None),
  key=getattr(settings, "PUSHER_APP_KEY", None),
  secret=getattr(settings, "PUSHER_APP_SECRET", None),
  cluster=getattr(settings, "PUSHER_APP_CLUSTER", None),
  ssl=True
)

@receiver(post_save, sender=Registration)
def my_handler(sender, instance, **kwargs):
    print("Sending count!")
    count = Registration.objects.count()
    event = instance.event
    pusher_client.trigger('event-' + event.slug, 'registration-event', {'count': count})
    print("Count sent to: ", 'event-' + event.slug, count)