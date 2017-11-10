from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .views import Select

urlpatterns = [
    url(r'^$', login_required(Select.as_view()), name='select'),
    ]