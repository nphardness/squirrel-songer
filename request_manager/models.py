from django.db import models

from repertoire_manager.models import PieceModel


class PieceRequestModel(models.Model):
    piece = models.ForeignKey(PieceModel, on_delete=models.CASCADE)
    requester = models.CharField(max_length=255, default='Anonymous')

    # we will sort by request_time, priority
    priority = models.IntegerField(default=10)  # decides about position in queue

    request_time = models.DateTimeField(auto_now_add=True)
    played = models.BooleanField(default=False)
    currently_playing = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {} {} played: {}'.format(
            str(self.piece), str(self.requester), str(self.priority),
            str(self.request_time), str(self.played))
