from django.core.management.base import BaseCommand

from modules.api.account.rsync_authorized_keys import regenerate_authorized_keys


class Command(BaseCommand):
    help = 'Rewrite the rsync authorized_keys file from current RsyncPublicKey rows.'

    def handle(self, *args, **options):
        regenerate_authorized_keys()
        self.stdout.write(self.style.SUCCESS('authorized_keys regenerated'))
