from django.shortcuts import render, redirect
from authentication.models import Logeado, Departament
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from authentication.views import NotCorporative

def Dashboard(request):
    if NotCorporative(request)== True:
        request.session['email']=request.user.email
        print('Not Corporative')
        data = {'title': 'Cuenta no corporativa',
                'messages': 'Su cuenta de correo es '+request.session['email']+' favor iniciar secion con cuenta adecuada.',
                'action': 'Cerrar Seccion'}
        return render(request, 'auth/error.html', data)
    else:
        user=Logeado.objects.get(user=request.user)

        request.session['fullname'] = user.user.first_name+' '+user.user.last_name
        request.session['username'] = user.user.username
        request.session['email'] = user.user.email
        request.session['new'] = user.new
        request.session['avatar'] = user.avatar
        try:
            if request.session['departament']['set'] != True:
                request.session['departament'] = {}
        except Exception as e:
            request.session['departament'] = {}
            request.session['departament']['set'] = True
            print(e)

        request.session['departament']['id'] = str(user.departament).split(",")
        request.session['departament']['active_id'] = user.set_departament
        request.session['departament']['active'] = Departament.objects.get(id=user.set_departament).name
        request.session['departament']['list'] =[]
        for lo in request.session['departament']['id']:
            if lo != "":
                request.session['departament']['list']+=[Departament.objects.get(id=int(lo)).name]

        request.session['alert'] = None

        if request.session['new'] == True:
            return redirect(reverse_lazy('auth:newuser'))

        #return render(request, 'dashboard/dashboard.html')
        return redirect(reverse_lazy('document:resume'))

def SetDepartament(request, name):
    user = Logeado.objects.get(user=request.user)
    user.set_departament=Departament.objects.get(name=name).id

    print(Logeado.objects.get(user=request.user).set_departament)
    user.save()
    print(Logeado.objects.get(user=request.user).set_departament)
    return Dashboard(request)