from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from authentication.models import Logeado
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from department.models import Departament
from authentication.forms import DeptoForm
from documents.models import Document_type
from corpcolina.settings import DEBUG

from django.views.generic.base import TemplateView

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


def newuser(request):
    NotCorporative(request)
    user = Logeado.objects.get(user=request.user)
    request.session['fullname'] = user.user.first_name + ' ' + user.user.last_name
    request.session['username'] = user.user.username
    request.session['email'] = user.user.email
    request.session['new'] = user.new
    request.session['avatar'] = user.avatar


    data={ 'departament' :Departament.objects.all().order_by('name')}

    if request.method == 'GET':
        data['form']= DeptoForm(instance=user)
    else:
        form = DeptoForm(request.POST, instance=user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.new = False
            dpt=str(obj.departament).split(",")
            dpo=""
            dps=""
            for dp in dpt:
                if dp != dps:
                    dps=dp
                    dp=dp+','
                    if dpo =="":
                        dpo=dp
                    else:
                        dpo = dpo+dp
            print(str(obj.departament)+' -- > '+dpo)
            obj.departament=dpo
            obj.set_departament=  Departament.objects.get(id=str(dpo).split(",")[0]).id
            request.session['new'] = False
            form.save()
        else:
            print(form.is_valid())
            print(form.errors)
            form = DeptoForm(request.POST)
        print(user)
        return redirect(reverse_lazy('dashboard:dashboard'))

    return render(request, 'auth/new_user.html', data)

