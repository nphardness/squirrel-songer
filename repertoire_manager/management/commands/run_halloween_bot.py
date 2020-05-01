from django.core.management.base import BaseCommand

from repertoire_manager.twitch_client.halloween_bot import TwitchClient


class Command(BaseCommand):
    help = 'Runs bot for repertoire'

    def handle(self, *args, **options):
        TwitchClient().run()
        self.stdout.write(self.style.SUCCESS(''))
