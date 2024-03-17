from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from procurement.models import Precurement_contractors, ContractorAward


@receiver(post_save, sender=Precurement_contractors)
def create_notification_for_contractor(sender, instance, **kwargs):
    recipient = instance.invite
    precurement_title = instance.precurement.title
    Notification.objects.create(
        user=recipient,
        message=f"You've been invited to the bidding of procurement titled: {precurement_title}"
    )


@receiver(post_save, sender=ContractorAward)
def award_notification_for_contractor(sender, instance, **kwargs):
    print(instance.contractors.all())
    for contractor in instance.contractors.all():
        recipient = contractor.account.user  
        procurement_title = instance.procurement.title
        Notification.objects.create(
            user=recipient,
            message=f"You've been awarded the procurement titled: {procurement_title}"
        )