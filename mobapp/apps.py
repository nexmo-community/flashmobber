from django.apps import AppConfig


class MobappConfig(AppConfig):
    name = 'mobapp'
    verbose_name = 'Nexmo FlashMobber'

    def ready(self):
        from . import signals
