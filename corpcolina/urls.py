"""corpcolina URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('dashboard.urls', namespace='dashboard')),
    url(r'^administrator/', include('App_Admin.urls', namespace='administrator')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^documentos/', include('documents.urls', namespace='document')),
    url(r'^ticket/', include('App_Ticket.urls', namespace='ticket')),
    url('^api/v1/', include('social_django.urls', namespace='social')),
    url('^auth/', include('authentication.urls', namespace='auth')),
    url(r'^accounts/login/', include('authentication.urls')),

]



urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render
def Verify(request):
    return render(request, 'verifyforzoho.html')

urlpatterns +=[
    url(r'^zohoverify/verifyforzoho.html$', Verify, name="verifyforzoho"),
]