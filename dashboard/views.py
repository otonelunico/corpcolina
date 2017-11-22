from django.shortcuts import render, redirect
from authentication.models import Logeado, Departament
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from authentication.views import NotCorporative

def Dashboard(request):
    if NotCorporative(request)== True:
        request.session['email']=request.user.email
        data = {'title': 'Cuenta no corporativa',
                'messages': 'Su cuenta de correo es '+request.session['email']+' favor iniciar secion con cuenta adecuada.',
                'action': 'Cerrar Seccion'}
        return render(request, 'auth/error.html', data)
    elif Logeado.objects.filter(user=request.user).count()>0:
        user=Logeado.objects.get(user=request.user)
        request.session['id'] = user.user.id
        if user.user.is_superuser:
            request.session['is_superuser'] = user.user.is_superuser
        request.session['fullname'] = user.user.first_name+' '+user.user.last_name
        request.session['username'] = user.user.username
        request.session['email'] = user.user.email
        request.session['phone'] = user.phone
        request.session['cellphone'] = user.cellphone
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
        request.session['departament']['active'] = { 'id' : Departament.objects.get(id=user.set_departament).id,
                                                     'name': Departament.objects.get(id=user.set_departament).name}
        request.session['departament']['list'] =[]
        for lo in request.session['departament']['id']:
            if lo != "":
                request.session['departament']['list']+=[{'id' : Departament.objects.get(id=int(lo)).id,
                                                         'name': Departament.objects.get(id=int(lo)).name}]
        print(request.session['departament']['list'])
        request.session['alert'] = None

        if request.session['new'] == True:
            return redirect(reverse_lazy('auth:newuser'))
        request.session['ticket'] = user.tick
        request.session['docs'] = user.docs
        #return render(request, 'dashboard/dashboard.html')
        if user.docs:
            return redirect(reverse_lazy('document:resume'))
        elif user.tick:
            return redirect(reverse_lazy('ticket:states'))
        else:
            return redirect(reverse_lazy('auth:newuser'))
    else:
        return redirect(reverse_lazy('auth:newuser'))


def SetDepartament(request, name):
    user = Logeado.objects.get(user=request.user)
    user.set_departament=Departament.objects.get(id=name).id

    print(Logeado.objects.get(user=request.user).set_departament)
    user.save()
    print(Logeado.objects.get(user=request.user).set_departament)
    return Dashboard(request)