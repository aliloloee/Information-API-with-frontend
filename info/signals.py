from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings

from .models import ECGInformation

@receiver(pre_delete, sender=ECGInformation)
def delete_ecg_file(sender, instance, using, **kwargs):
    media_url = settings.MEDIA_URL
    try :
        ecg = instance.ecg.url
        path = ecg.strip(media_url)
        default_storage.delete(path)
    except :
        pass