from django.db import models


class PieceStatus:
    NEW = 'NEW'
    PROGRESS = 'PROGRESS'
    REJECTED = 'REJECTED'
    DONE = 'DONE'
    STATUS = (
        (NEW, 'new'),
        (PROGRESS, 'in progress'),
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

    TYPE = (
        (MOVIE, 'movie'),
        (CLASSICAL, 'classical'),
        (ANIME, 'anime'),
        (GAME, 'game'),
        (TRANSCRIPTION, 'transcription'),
        (OTHER, 'other')
    )


class PieceModel(models.Model):
    """
    For movie, anime, game - title is the name of the entity.
    """

    composer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=PieceStatus.STATUS, default=PieceStatus.NEW)
    type = models.CharField(max_length=32, choices=PieceType.TYPE, default=PieceType.OTHER)
    number_of_requests = models.IntegerField(default=0)

    level = models.IntegerField(null=True, blank=True)
    last_played = models.DateTimeField(null=True, blank=True)
    movement = models.CharField(max_length=32, null=True, blank=True)
    nick = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.composer) + ' - ' + str(self.title) + ' ' + str(self.movement)
