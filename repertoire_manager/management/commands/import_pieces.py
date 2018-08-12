import json

from django.core.management.base import BaseCommand, CommandError
from repertoire_manager.models import PieceModel, PieceType


class Command(BaseCommand):
    help = 'Imports pieces from json got from StreamerSongList page'
    attributes_ids = {
        'game': 1032,
        'transcription': 1031,
        'other': 1030,
        'anime': 1029,
        'movie': 1028,
        'classical': 1027,
        'hard':  1035
    }

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def _save_piece(self, piece, db_pieces, piece_type: PieceType, level=None):
        for db_piece in db_pieces:
            if piece['artist'] == db_piece.composer:
                if db_piece.title in piece['name']:
                    self.stdout.write(
                        self.style.WARNING('Already imported %s %s' % (piece, db_piece)))
                    return False
        new_piece = PieceModel(
            composer=piece['artist'],
            title=piece['name'],
            type=piece_type,
            number_of_requests=piece['timesPlayed'],
            level=level,
            last_played=piece['lastPlayed'],
            comment='Imported from StreamerSongList %s' % str(piece))
        new_piece.save()
        return True

    def _save_pieces(self, pieces: list) -> int:
        """
        Each pieces has keys:
        ['id', 'name', 'artist', 'createdAt', 'learned', 'active',
        'StreamerId', 'bypassRequestLimit', 'attributes', 'timesPlayed',
        'lastPlayed', 'isNew', 'inQueue'])
        :param pieces:
        :return:
        """
        number_of_imported_pieces = 0

        db_pieces = PieceModel.objects.all()
        for piece in pieces:
            if_saved = False
            level = 10 if self.attributes_ids['hard'] in piece['attributes'] else None
            if self.attributes_ids['classical'] in piece['attributes']:
                if_saved = self._save_piece(piece, db_pieces, PieceType.CLASSICAL, level=level)
            elif self.attributes_ids['game'] in piece['attributes']:
                if_saved = self._save_piece(piece, db_pieces, PieceType.GAME, level=level)
            elif self.attributes_ids['movie'] in piece['attributes']:
                if_saved = self._save_piece(piece, db_pieces, PieceType.MOVIE, level=level)
            elif self.attributes_ids['anime'] in piece['attributes']:
                if_saved = self._save_piece(piece, db_pieces, PieceType.ANIME, level=level)
            elif self.attributes_ids['transcription'] in piece['attributes']:
                if_saved = self._save_piece(piece, db_pieces, PieceType.TRANSCRIPTION, level=level)
            else:
                if_saved = self._save_piece(piece, db_pieces, PieceType.OTHER, level=level)
            if if_saved:
                number_of_imported_pieces += 1
            else:
                self.stdout.write(
                    self.style.WARNING('Did not import piece %s' % piece))

        return number_of_imported_pieces

    def handle(self, *args, **options):
        with open(options['path'], 'r') as f:
            pieces = json.loads(f.read())

        number_of_imported_pieces = self._save_pieces(pieces)

        self.stdout.write(self.style.SUCCESS('Imported %s pieces' % number_of_imported_pieces))
