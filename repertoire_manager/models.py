from django.db import models


class PieceStatus:
    NEW = 'NEW'
    PROGRESS = 'PROGRESS'
    REJECTED = 'REJECTED'
    INACTIVE = 'INACTIVE'
    DONE = 'DONE'
    STATUS = (
        (NEW, 'new'),
        (PROGRESS, 'in progress'),
        (INACTIVE, 'inactive'),
        (REJECTED, 'rejected'),
        (DONE, 'done'),
    )


class PieceType:
    MOVIE = 'MOVIE'
    CLASSICAL = 'CLASSICAL'
    ANIME = 'ANIME'
    GAME = 'GAME'
    TRANSCRIPTION = 'TRANSCRIPTION'
    OTHER = 'OTHER'
    HALLOWEEN = 'HALLOWEEN'

    TYPE = (
        (MOVIE, 'movie'),
        (CLASSICAL, 'classical'),
        (ANIME, 'anime'),
        (GAME, 'game'),
        (TRANSCRIPTION, 'transcription'),  # TODO: remove transcription
        (OTHER, 'other'),
        (HALLOWEEN, 'halloween'))


class PieceModel(models.Model):
    """
    For movie, anime, game - title is the name of the entity.
    """

    s_id = models.IntegerField(default=-1)  # id from streamerssonglist - to remove when not used anymore
    composer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=PieceStatus.STATUS, default=PieceStatus.NEW)

    number_of_requests = models.IntegerField(default=0)

    level = models.IntegerField(null=True, blank=True)
    last_played = models.DateTimeField(null=True, blank=True)
    movement = models.CharField(max_length=32, null=True, blank=True)
    nick = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.composer) + ' - ' + str(self.title) + ' ' + str(self.movement)

    def str_for_txt(self):
        if self.movement:
            return str(self)
        else:
            return str(self.composer) + ' - ' + str(self.title)


class PieceTags(models.Model):
    piece_id = models.ForeignKey(PieceModel, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=32, choices=PieceType.TYPE, default=PieceType.OTHER)
    s_id = models.IntegerField(default=-1)  # id from streamersonglist