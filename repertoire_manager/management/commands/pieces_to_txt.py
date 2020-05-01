from django.core.management.base import BaseCommand
from django.db.models import Q

from repertoire_manager.models import PieceModel, PieceStatus


class Command(BaseCommand):
    help = 'Export pieces to readable format'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    @staticmethod
    def get_pieces_text():
        inactive_pieces = PieceModel.objects.filter(
            status=PieceStatus.INACTIVE).order_by('type', 'composer', 'title').all()
        active_pieces = PieceModel.objects.filter(
            ~Q(status=PieceStatus.INACTIVE)).order_by('type', 'composer', 'title').all()
        titles_pieces = {'Repertoire': active_pieces, 'Repertoire in preparation': inactive_pieces}
        pieces_str = ''
        for title, pieces in titles_pieces.items():
            if not pieces_str:
                pieces_str += title + '\n\n'
            else:
                pieces_str += '\n\n' + title + '\n\n'
            last_piece_type = None
            for piece in pieces:
                if 'Live Learn' in piece.title:
                    continue
                if last_piece_type != piece.type:
                    last_piece_type = piece.type
                    pieces_str += '\n' + last_piece_type + '\n\n'
                pieces_str += piece.str_for_txt() + '\n'
        return pieces_str

    def handle(self, *args, **options):
        if options['path']:
            with open(options['path'], 'w') as f:
                f.write(self.get_pieces_text())
        else:
            print(self.get_pieces_text())

        self.stdout.write(self.style.SUCCESS(''))
