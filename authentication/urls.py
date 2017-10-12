from .views import index, logout, Newuser, ErrorPage
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^logout$', login_required(logout), name='logout'),
    url(r'^newuser$', login_required(Newuser.as_view()), name='newuser'),
    url(r'^error_page$',ErrorPage.as_view(), name='error_page')
]