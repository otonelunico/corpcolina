from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from authentication.models import Logeado
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from department.models import Departament
from authentication.forms import TransferForm
from documents.models import Document_type
from corpcolina.settings import DEBUG

from django.views.generic.base import TemplateView
from django.views import View
from django.core.mail import send_mail


class ErrorPage(TemplateView):
    template_name = 'auth/error.html'


def index(request):
    return render(request, 'index.html')

def Set_data(request, backend, strategy, details, is_new, response,
               *args, **kwargs):
    user = User.objects.get(username=details['username'])
    if str(user.email).split("@")[1] == 'gmail.com':
        print('gmail')
    else:
        if Logeado.objects.filter(user=user):
            ll = Logeado.objects.get(user=user)
            print('entro no nuevo -- aki 1 --> '+str(ll))
            ll.avatar = None
            if backend.name == 'google-oauth2':
                ll.avatar = response['image'].get('url')
            ll.online = True
            ll.save()

            print('fin')

        else:
            print('entro nuevo')
            avatar = None
            if backend.name == 'google-oauth2':
                avatar = response['image'].get('url')
            user = User.objects.get(username=details['username'])

            if Departament.objects.filter(id=1).count() < 1:
                Departament.objects.create(name='Defauld',
                                           description='Inicial'
                                           )
            if User.objects.all().count()<2:
                user.is_staff=True
                user.save()
                Document_type.objects.create(titulo = 'Oficio')
            print(user.is_staff)
            Logeado.objects.create(user = user,
                                    new = True,
                                    avatar=avatar,
                                    departament=1,
                                    set_departament = 1,
                                    online = True)

    print('Salio')

from django.contrib.sessions.models import Session

def logout(request):
    if NotCorporative(request):
        print(request)
    else:
        user=Logeado.objects.get(user = request.user)
        user.online = False
        user.save()

    for key in list(request.session.keys()):
        del request.session[key]
    auth_logout(request)
    return render(request, 'auth/logout.html')


def NotCorporative(request):
    if str(User.objects.get(username=request.user).email).split("@")[1] != 'corporacioncolina.cl':

        return True


class Newuser(View):
    template = 'auth/new_user.html'
    departament = Departament.objects.all().order_by('name')

    def get(self, request):
        NotCorporative(request)
        user = Logeado.objects.get(user=request.user)
        request.session['fullname'] = user.user.first_name + ' ' + user.user.last_name
        request.session['username'] = user.user.username
        request.session['email'] = user.user.email
        request.session['new'] = user.new
        request.session['avatar'] = user.avatar
        departament = self.departament
        return render(request, self.template, locals())

    def post(self, request, **kwargs):

        departament = self.departament
        user = Logeado.objects.get(user=request.user)
        form = TransferForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            print(obj.transfer)
            tra = obj.transfer.split(';')
            tra += [user]
            print(tra[5].id)
            """send_mail("Solicitud",
                      "Mensaje...nLinea 2nLinea3",
                      '"origen" <origen@example.com>',
                      ['ocubillos@corporacioncolina.cl'],
                      fail_silently=False)"""
            print(tra)
            #request.session['new'] = False
            #form.save()
        else:
            print(form.is_valid())
            print(form.errors)
            form = TransferForm(request.POST)
        return render(request, self.template, locals())

