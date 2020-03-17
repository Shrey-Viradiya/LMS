from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, Availability


@receiver(post_save, sender=Book)
def create_availability(sender, instance, created, **kwargs):
    if created:
        Availability.objects.create(ISBN=instance.ISBN, availability=kwargs['availability'])


@receiver(post_save, sender=Book)
def save_availability(sender, instance, **kwargs):
    instance.profile.save()
