from django.urls import path

from .views import StreamQueueView, PieceRequestUpdateView, \
    PieceRequestPriorityUpdateView, PieceRequestCreateView, PiecesListView, Home, HistoryView

from django.contrib.auth import views as auth_views
app_name = 'request_manager'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('queue/', StreamQueueView.as_view(), name='queue'),
    path('history/', HistoryView.as_view(), name='history'),
    path('pieces-list/', PiecesListView.as_view(), name='pieces-list'),
    path('piece-request-update/<int:piece_request_id>/', PieceRequestUpdateView.as_view(),
         name='piece-request-update'),

    path('piece-request-priority-update/<int:piece_request_id>/',
         PieceRequestPriorityUpdateView.as_view(), name='piece-request-priority-update'),
    path('piece-request-create/<int:piece_id>/', PieceRequestCreateView.as_view(),
         name='piece-request-create'),
    path(r'login/', auth_views.login,  {'template_name': 'login.html'}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
]
