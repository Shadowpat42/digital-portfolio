from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def set_superuser_status(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.is_staff = True
        instance.save()


@receiver(pre_delete, sender=get_user_model())
def prevent_superuser_deletion(sender, instance, **kwargs):
    if instance.is_superuser:
        return False
