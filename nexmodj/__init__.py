from django.conf import settings

import nexmo


default_app_config = 'nexmodj.apps.NexmodjConfig'

client = nexmo.Client(
    api_key=getattr(settings, "NEXMO_API_KEY", None),
    api_secret=getattr(settings, "NEXMO_API_SECRET", None),
    signature_secret=getattr(settings, "NEXMO_SIGNATURE_SECRET", None),
    signature_method=getattr(settings, "NEXMO_SIGNATURE_METHOD", None),
    application_id=getattr(settings, "NEXMO_APPLICATION_ID", None),
    private_key=getattr(settings, "NEXMO_PRIVATE_KEY", None),
)

