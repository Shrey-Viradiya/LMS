from datetime import timedelta

from django.apps import AppConfig


class LibrarymsConfig(AppConfig):
    name = 'LibraryMS'

    def ready(self):
        from .tasks import SendEmails
        # SendEmails(schedule=timedelta(seconds=3), repeat=86400)
