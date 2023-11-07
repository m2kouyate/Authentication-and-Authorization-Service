from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser, UserProfile
from django.core.files.storage import FileSystemStorage
from django.conf import settings

user_storage = FileSystemStorage(location=settings.MEDIA_ROOT / 'user_profiles')


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()


@receiver(post_delete, sender=UserProfile)
def delete_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)
