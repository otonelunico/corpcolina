from dashboard.views import Dashboard, SetDepartament
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(Dashboard), name='dashboard'),
    url(r'^setdepartament/(?P<name>\w+)$',login_required(SetDepartament), name='SetDepartament'),
]