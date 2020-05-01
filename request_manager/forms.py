from django import forms

from repertoire_manager.models import PieceModel


class PieceRequestUpdateForm(forms.Form):
    played = forms.BooleanField(label='played')


class PieceRequestPriorityUpdateForm(forms.Form):
    priority = forms.IntegerField(label='priority')


class PieceRequestCreateForm(forms.Form):
    piece = forms.ModelChoiceField(queryset=PieceModel.objects.all())
    requester = forms.CharField()
