from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Media, MediaPlatform
from .services import handle_platform_upload


@receiver(pre_save, sender=Media)
def handle_copyright_flag(sender, instance, **kwargs):
    """
    If a media item is flagged for copyright, automatically set its privacy to private.
    """
    if instance.pk:
        try:
            old_instance = Media.objects.get(pk=instance.pk)
            # If it wasn't flagged before but is now
            if instance.copyright_flagged and not old_instance.copyright_flagged:
                instance.privacy = "private"
        except Media.DoesNotExist:
            pass
    # New instance that is flagged immediately
    elif instance.copyright_flagged:
        instance.privacy = "private"


@receiver(post_save, sender=MediaPlatform)
def trigger_platform_upload(sender, instance, created, **kwargs):
    """
    Trigger upload to external platform when MediaPlatform is created.
    """
    if created and not instance.uploaded:
        handle_platform_upload(instance)
