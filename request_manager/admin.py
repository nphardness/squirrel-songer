from django.contrib import admin

from request_manager.models import PieceRequestModel


class StreamQueueAdmin(admin.ModelAdmin):
    list_display = ('stream', 'start_time', )


class PieceRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'piece', 'priority', 'played')


admin.site.register(PieceRequestModel, PieceRequestAdmin)
