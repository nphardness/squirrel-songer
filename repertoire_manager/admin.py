from django.contrib import admin

from repertoire_manager.models import PieceModel


class PieceAdmin(admin.ModelAdmin):
    list_display = ('composer', 'title', 'level', 'status', 'number_of_requests', 'last_played',
                    'movement', 'nick', 'comment')


admin.site.register(PieceModel, PieceAdmin)