from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from authentication.models import Logeado
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from department.models import Departament
from authentication.forms import TransferForm
from documents.models import Document_type
from corpcolina.settings import DEBUG
from App_Admin.models import Req

from django.views.generic.base import TemplateView
from django.views import View
from django.core.mail import send_mail


class ErrorPage(TemplateView):
    template_name = 'auth/error.html'

def index(request):
    return render(request, 'index.html')

def Set_data(request, backend, strategy, details, is_new, response, *args, **kwargs):
    print(kwargs['user'])
    #user = User.objects.get(username=details['username'])
    if kwargs['uid'].split("@")[1] == 'corporacioncolina.cl':
        if Logeado.objects.filter(user__username=str(kwargs['user'])).count()>0:
            ll = Logeado.objects.get(user__username=str(kwargs['user']))
            print('entro no nuevo -- aki 1 --> '+str(ll))
            ll.avatar = None
            if backend.name == 'google-oauth2':
                ll.avatar = response['image'].get('url')
            ll.online = True
            ll.save()


        else:
            print('entro nuevo')
            avatar = None
            if backend.name == 'google-oauth2':
                avatar = response['image'].get('url')
            user = User.objects.get(username=str(kwargs['user']))

            if Departament.objects.filter(id=1).count() < 1:
                Departament.objects.create(name='Defauld',
                                           description='Inicial'
                                           )
            if User.objects.all().count()<2:
                user.is_staff=True
                user.save()
                Document_type.objects.create(titulo = 'Oficio')
            Logeado.objects.create(user = user,
                                    new = True,
                                    avatar=avatar,
                                    departament=1,
                                    set_departament = 1,
                                    online = True)

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
        if Logeado.objects.filter(user=request.user).count()>0:
            user = Logeado.objects.get(user=request.user)
            user.new = True
            user.save()
        else:
            user = Logeado.objects.create(user=request.user)
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
        user.new = True
        user.save()
        form = TransferForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            print(obj.transfer)
            tra = obj.transfer.replace('false', 'False')
            tra = tra.replace('true', 'True')
            tra = tra.split(';')
            tra += [user]
            print(tra)
            if Req.objects.filter(user=user).count() >0:
                req = Req.objects.get(user=user)
                req.dpts = tra[0]
                req.docs = tra[1]
                req.tick = tra[2]
                req.admin = tra[3]
                req.coment = tra[4]
                req.save()
            else:
                Req.objects.create(
                dpts = tra[0],
                docs = tra[1],
                tick = tra[2],
                admin = tra[3],
                coment = tra[4],
                user = tra[5],
            )

            #request.session['new'] = False
            #form.save()
        else:
            print(form.is_valid())
            print(form.errors)
            form = TransferForm(request.POST)
        return redirect(reverse_lazy('auth:espera'))

def userAdmin(request):
    if Logeado.objects.get(user=request.user).admin:
        return True

def userDocs(request):
    if Logeado.objects.get(user=request.user).docs:
        return True

class Espera(View):
    template = 'auth/espera.html'

    def get(self, request):
        #user = Logeado.objects.get(user=request.user)
        print(Logeado.objects.get(user=request.user).new)
        if Logeado.objects.get(user=request.user).new == False:
            return redirect(reverse_lazy('dashboard:dashboard'))
        return render(request, self.template, locals())