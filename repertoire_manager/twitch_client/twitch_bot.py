import random
import re
import socket

from django.conf import settings
import requests

from repertoire_manager.models import PieceModel, PieceType


class TwitchClient(object):

    def __init__(self):
        self.piece_request = PieceRequest()
        self.con = socket.socket()
        self.CHAN = settings.TWITCH_BOT_CHANNEL
        self.HOST = settings.TWITCH_HOST
        self.PORT = settings.TWITCH_PORT
        self.NICK = settings.TWITCH_BOT_NICK
        self.PASS = settings.TWITCH_BOT_OAUTH
        self.con.connect((self.HOST, self.PORT))

        self.send_pass(self.PASS)
        self.send_nick(self.NICK)
        self.join_channel(self.CHAN)

    def send_pong(self, msg):
        self.con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_message(self, msg):
        self.con.send(bytes('PRIVMSG %s :%s\r\n' % (self.CHAN, msg), 'UTF-8'))

    def send_nick(self, nick):
        self.con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))

    def send_pass(self, password):
        self.con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

    def join_channel(self, chan):
        self.con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

    def part_channel(self, chan):
        self.con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
        
    def run(self):
        data = ""

        while True:
            data = ''
            try:
                data = data+self.con.recv(1024).decode('UTF-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()

                for line in data_split:
                    line = str.rstrip(line)
                    line = str.split(line)

                    if len(line) >= 1:
                        if line[0] == 'PING':
                            self.send_pong(line[1])

                        if line[1] == 'PRIVMSG':
                            sender = self.get_sender(line[0])
                            message = self.get_message(line)
                            try:
                                self.parse_message(message, sender)
                            except Exception as e:
                                print(e)
                            print(sender + ": " + message)

            except socket.error:
                print("Socket died")

            except socket.timeout:
                print("Socket timeout")

    @classmethod
    def get_sender(cls, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        return result

    @classmethod
    def get_message(cls, msg):
        result = ""
        i = 3
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        return result

    def parse_message(self, msg, sender):
        if len(msg) >= 1:
            msg = msg.split(' ')
            # options = {'!songlist': self.command_song, '!sr': self.command_song_request, '!test': self.command_test} # TODO: change that back
            options = {'!halloweenRequest': self.command_halloween_request, '!halloween': self.command_halloween}
            if msg[0] in options:
                response = options[msg[0]](msg, sender)
                self.send_message(response)

    def command_halloween(self, msg, sender):
        pieces = list(PieceModel.objects.filter(type=PieceType.HALLOWEEN).all())
        pieces = ['{}'.format(p.title) for p in pieces]
        resp = '@{}, use !halloweenRequest - request random halloween piece!'.format(sender) + ' Pieces: ' + ', '.join(pieces)
        return resp

    def command_halloween_request(self, msg, sender):
        headers = {'Authorization': settings.STREAMER_SONGLIST_TOKEN} #, 'content-type': 'application/json'}
        url = 'https://api.streamersonglist.com/api/streamers/{}/queues'.format(
            settings.STREAMER_ID)
        print(sender)

        if len(self.halloween_pieces) == len(self.halloween_played_ids):
            self.halloween_played_ids = []
        random_idx = random.randint(0, len(self.halloween_pieces)-1)
        while self.halloween_pieces[random_idx].s_id in self.halloween_played_ids:
            random_idx = random.randint(0, len(self.halloween_pieces) - 1)

        r = {
            "requests": [{'name': sender, 'amount':0}],
            'name': sender,
            "donationAmount": 0,
            "note": "halloween",
            "StreamerId": 105,
            "SongId": self.halloween_pieces[random_idx].s_id
        }
        resp = requests.post(url, json=r, headers=headers)

        if resp.status_code < 400:
            print(resp.json())
            self.halloween_played_ids.append(self.halloween_pieces[random_idx].s_id)
            return 'Added {} - {}'.format(self.halloween_pieces[random_idx].composer, self.halloween_pieces[random_idx].title)
        else:
            print(resp.status_code, resp.json())
            return 'It seems my random numbers generator does not like me...'

    def command_test(self, msg, sender):
        return 'testing'

    def command_song(self, msg, sender): # TODO: rename -> it's a pieces list
        composer = self.piece_request.get_pieces_by_composer(msg[1])
        if composer:
            return 'Pieces by {}: fur elise'.format(composer)
        elif msg[1]:
            return 'Not found any pieces by {}'.format(msg[1])
        else:
            return 'Full pieces list is not available yet!'

    def command_song_request(self, msg, sender):
        if msg[1]:
            return 'Song requests are not implemented yet!' # TODO: remove it after implementing functionality
        if msg[1]: 
            parsed_song = self.piece_request.get_piece(msg[1])
            if parsed_song:
                return '{} requested piece: {}. Found: {}'.format(sender, msg[1], parsed_song)
            else:
                return '{} requested piece: {}. Not found :(. Use !songlist [composer] to check the pieces list'.format(
                    sender, msg[1], parsed_song)
        else:
            return ''


