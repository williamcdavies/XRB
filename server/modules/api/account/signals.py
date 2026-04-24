import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from modules.api.account.models import RsyncPublicKey
from modules.api.account.rsync_authorized_keys import regenerate_authorized_keys

log = logging.getLogger(__name__)


def _safe_regenerate():
    try:
        regenerate_authorized_keys()
    except Exception:
        log.exception('failed to regenerate rsync authorized_keys')


@receiver(post_save, sender=RsyncPublicKey)
def _rsync_key_saved(sender, instance, **kwargs):
    _safe_regenerate()


@receiver(post_delete, sender=RsyncPublicKey)
def _rsync_key_deleted(sender, instance, **kwargs):
    _safe_regenerate()
