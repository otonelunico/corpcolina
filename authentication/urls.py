from authentication.views import index, logout, newuser
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from authentication.views import ErrorPage

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout$', login_required(logout), name='logout'),
    url(r'^newuser$', login_required(newuser), name='newuser'),
    url(r'^error_page$',ErrorPage.as_view(), name='error_page')
]