from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import State, NewTicket,NewData, DetailTicket, ListTicket

urlpatterns = [
    url(r'^$', login_required(State.as_view()), name='states'),
    url(r'^new/$', login_required(NewTicket.as_view()), name='new'),
    url(r'^new/data/(?P<value>\w+)$', login_required(NewData.as_view()), name='new_data'),
    url(r'^detail/(?P<id>\d+)$', login_required(DetailTicket.as_view()), name='detail'),
    url(r'^list/$', login_required(ListTicket.as_view()), name='list'),
]