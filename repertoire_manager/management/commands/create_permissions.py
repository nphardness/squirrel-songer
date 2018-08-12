from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from repertoire_manager.models import PieceModel
from request_manager.models import PieceRequestModel


class Command(BaseCommand):
    help = 'Creates permissions for models'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(PieceModel)
        permission = Permission.objects.create(
            codename='can_edit',
            name='Can edit pieces',
            content_type=content_type,
        )
        permission.save()

        content_type = ContentType.objects.get_for_model(PieceRequestModel)
        permission = Permission.objects.create(
            codename='can_edit',
            name='Can edit pieces request',
            content_type=content_type,
        )
        permission.save()

        self.stdout.write(self.style.SUCCESS('Created'))


