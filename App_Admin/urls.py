from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import export_users_xls, Select, Register

urlpatterns = [
    url(r'^$', login_required(Select.as_view()), name='select'),
    url(r'^register/(?P<id>\d+)/(?P<docs>\w+)/(?P<tick>\w+)/(?P<admin>\w+)/(?P<dpts>\w+)$', login_required(Register.as_view()), name='register'),
    url(r'^export/xls/$', export_users_xls, name='export_users_xls'),
    ]