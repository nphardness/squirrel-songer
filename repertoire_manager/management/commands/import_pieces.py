import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from repertoire_manager.models import PieceModel, PieceStatus, PieceTags


class Command(BaseCommand):
    help = 'Imports pieces from json got from StreamerSongList page'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
        parser.add_argument('--api', type=bool)  # TODO: it should not require arg

    def _save_piece(self, piece, db_pieces, status=PieceStatus.NEW, attributes=None):
        for db_piece in db_pieces:
            if piece['artist'] == db_piece.composer:
                if db_piece.title in piece['name']:
                    self.stdout.write(
                        self.style.WARNING('Already imported %s %s' % (piece, db_piece)))
                    return False
        new_piece = PieceModel(
            s_id=piece['id'],
            composer=piece['artist'],
            title=piece['name'],
            status=status,
            number_of_requests=piece['timesPlayed'],
            last_played=piece['lastPlayed'],
            comment='Imported from StreamerSongList %s' % str(piece))
        new_piece.save()
        print(attributes)
        print(attributes)
        for piece_attr in piece['attributes']:
            name = ''
            for attr in attributes:
                if attr['id'] == piece_attr:
                    name = attr['name']
            piece_tag = PieceTags(
                s_id=piece_attr,
                type=name,
                piece_id=new_piece)
            piece_tag.save()
        return True

    def _save_pieces(self, pieces: list, attributes) -> int:
        """
        Each piece from streamersonglist has keys:
        ['id', 'name', 'artist', 'createdAt', 'learned', 'active',
        'StreamerId', 'bypassRequestLimit', 'attributes', 'timesPlayed',
        'lastPlayed', 'isNew', 'inQueue'])
        """
        number_of_imported_pieces = 0

        db_pieces = PieceModel.objects.all()
        for piece in pieces:
            is_new = piece['isNew']
            is_active = piece['active']
            status = PieceStatus.NEW
            if is_new:
                status = PieceStatus.NEW
            if not is_active:
                status = PieceStatus.INACTIVE  # that's is ok to overwrite new status

            if_saved = self._save_piece(
                piece, db_pieces, status=status, attributes=attributes)

            if if_saved:
                number_of_imported_pieces += 1
            else:
                self.stdout.write(
                    self.style.WARNING('Did not import piece %s' % piece))

        return number_of_imported_pieces

    @staticmethod
    def get_pieces_from_streamer_songlist():
        headers = {'Authorization': settings.STREAMER_SONGLIST_TOKEN}

        url = 'https://api.streamersonglist.com/api/streamers/{}/songs?showInactive=true'.format(
            settings.STREAMER_ID)
        r = requests.get(url, headers=headers)
        pieces = r.json()['items']
        with open('pieces.json', 'w') as f:
            f.write(json.dumps(pieces))
        return pieces

    def handle(self, *args, **options):
        pieces = None
        headers = {'Authorization': settings.STREAMER_SONGLIST_TOKEN}
        url_attributes = f'https://api.streamersonglist.com/api/users/{settings.STREAMER_NAME}'
        r = requests.get(url_attributes, headers=headers)
        attributes = r.json()['streamer']['attributes']

        if options['api']:
            pieces = self.get_pieces_from_streamer_songlist()
        elif options['path']:
            with open(options['path'], 'r') as f:
                pieces = json.loads(f.read())
        else:
            self.stdout.write(
                self.style.ERROR('You must determine if reading pieces from json or from api'))
            return
        number_of_imported_pieces = self._save_pieces(pieces, attributes)

        self.stdout.write(self.style.SUCCESS('Imported %s pieces' % number_of_imported_pieces))
