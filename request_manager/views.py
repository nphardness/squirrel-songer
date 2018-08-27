from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import QueryDict, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, FormView, CreateView

from repertoire_manager.models import PieceModel
from request_manager.forms import PieceRequestUpdateForm, PieceRequestPriorityUpdateForm, \
    PieceRequestCreateForm
from request_manager.models import PieceRequestModel


class Home(ListView):
    template_name = 'home.html'
    context_object_name = 'pieces_list'

    model = PieceModel  # TODO: it's not using any info, but maybe it could show favorites :)


class PiecesListView(ListView):
    template_name = 'pieces_list.html'
    context_object_name = 'pieces_list'

    model = PieceModel

    @staticmethod
    def _convert_to_piece_dict(piece: PieceModel) -> dict:
        last_played = piece.last_played
        if last_played:
            last_played = piece.last_played.strftime('%d-%m-%Y')
        else:
            last_played = '---'
        piece_dict = {
            'id': piece.id,
            'title': piece.title,
            'composer': piece.composer,
            'nick': piece.nick,
            'type': str(piece.type).lower(),
            'hard': piece.level is not None and piece.level >= 8,  # TODO: add permission for that!
            'last_played': last_played,
            'status': piece.status,
            'number_of_requests': piece.number_of_requests,
        }
        return piece_dict

    def _convert_to_pieces(self, pieces):
        pieces_list = []
        for p in pieces:
            pieces_list.append(self._convert_to_piece_dict(p))
        return pieces_list

    def get_context_data(self, **kwargs):
        pieces = PieceModel.objects.order_by('composer', 'title') # TODO: ordering list, custom filters
        active_pieces = list(pieces.filter(active=True).all())

        inactive_pieces = list(pieces.filter(active=False).all())
        active_pieces = self._convert_to_pieces(active_pieces)
        inactive_pieces = self._convert_to_pieces(inactive_pieces)

        context = {
            'pieces': active_pieces,
            'inactive_pieces': inactive_pieces
        }
        return context


class StreamQueueView(ListView):
    template_name = 'queue.html'
    context_object_name = 'stream_queue'

    model = PieceRequestModel

    @staticmethod
    def _convert_to_piece_request_dict(piece: PieceRequestModel) -> dict:
        last_played = piece.piece.last_played
        if last_played:
            last_played = piece.piece.last_played.strftime('%d-%m-%Y')
        else:
            last_played = '---'
        piece_dict = {
            'id': piece.piece.id,
            'title': piece.piece.title,
            'composer': piece.piece.composer,
            'nick': piece.piece.nick,
            'requester': piece.requester,
            'request_time': piece.request_time.strftime('%d-%m-%Y'),
            'last_played': last_played,
            'status': piece.piece.status,
            'played': piece.played,
            'type': str(piece.piece.type).lower(),
            'hard': piece.piece.level is not None and piece.piece.level >= 8,
            'priority': piece.priority,
            'currently_playing': piece.currently_playing,
            'request_id': piece.id,
        }
        return piece_dict

    def _convert_to_pieces_requests(self, pieces):
        pieces_list = []
        for p in pieces:
            pieces_list.append(self._convert_to_piece_request_dict(p))
        return pieces_list

    def get_context_data(self, **kwargs):
        pieces = PieceRequestModel.objects.order_by('-priority', 'request_time')
        played_pieces = list(pieces.filter(played=True).all())

        pieces = list(pieces.filter(played=False).all())
        pieces = self._convert_to_pieces_requests(pieces)
        played_pieces = self._convert_to_pieces_requests(played_pieces)

        context = {
            'pieces': pieces,
            'played_pieces': played_pieces
        }
        return context


class HistoryView(StreamQueueView):
    template_name = 'history.html'  # TODO: view only from today or all time or filters?


class PieceRequestUpdateView(FormView):
    template_name = 'queue.html'
    form_class = PieceRequestUpdateForm

    def post(self, request: WSGIRequest, *args, **kwargs):
        piece_request = PieceRequestModel.objects.filter(id=kwargs['piece_request_id']).first()
        if not piece_request.played:
            piece = piece_request.piece
            piece.last_played = datetime.now()
            piece.save()
        piece_request.played = not piece_request.played
        piece_request.save()
        return super(PieceRequestUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_manager:queue')


class PieceRequestPriorityUpdateView(FormView):
    template_name = 'queue.html'
    form_class = PieceRequestPriorityUpdateForm

    def post(self, request: WSGIRequest, *args, **kwargs):
        piece_request = PieceRequestModel.objects.filter(id=kwargs['piece_request_id']).first()
        data = QueryDict(request.body)
        piece_request.priority = data.get('priority')
        piece_request.save()
        return super(PieceRequestPriorityUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_manager:queue')


class PieceRequestCreateView(FormView):
    template_name = 'pieces_list.html'
    form_class = PieceRequestCreateForm

    def post(self, request: WSGIRequest, *args, **kwargs):
        # TODO: what if request is already in the queue? add requester!
        piece = PieceModel.objects.filter(id=kwargs['piece_id']).first()
        data = QueryDict(request.body)
        print(data)
        piece_request = PieceRequestModel(piece=piece, requester=data.get('requester'))
        piece_request.save()
        super(PieceRequestCreateView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('request_manager:queue'))  # TODO: success message

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_manager:queue')

# TODO: fix http://localhost:8000/accounts/email/