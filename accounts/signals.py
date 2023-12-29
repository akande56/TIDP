from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from procurement.models import Precurement_contractors


@receiver(post_save, sender=Precurement_contractors)
def create_notification_for_contractor(sender, instance, **kwargs):
    recipient = instance.invite
    precurement_title = instance.precurement.title
    print('singla called....')
    Notification.objects.create(
        user=recipient,
        message=f"You've been invite to the procurement: {precurement_title}"
    )