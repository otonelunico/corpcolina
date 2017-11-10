from django.shortcuts import render
from .models import Req
from django.contrib.auth.models import User
from authentication.models import Logeado
from department.models import Departament
from django.views import View
from .forms import ReqForm

# Create your views here.

class Select(View):
    template = 'admin/select.html'

    def icon(self, status):
        if status:
            return 'check'
        else:
            return 'close'
    def get(self, request):
        req = Req.objects.filter(active=True).order_by('id')
        form = ReqForm()
        for re in req:
           re.admin = self.icon(re.admin)
           re.tick = self.icon(re.tick)
           re.docs = self.icon(re.docs)


        users = Logeado.objects.all()
        dep = Departament.objects.all()
        for ll in req:
            lo = str(ll.dpts)
            lo = lo.split(',')
            ll.dpts = []
            for ls in lo:
                for le in dep:
                    if int(ls) == le.id:
                        ll.dpts += [le]
        for ll in users:
            if ll.departament != ',':
                lo = ll.departament
            lo = lo.split(',')
            ll.departament = []
            for ls in lo:
                for le in dep:
                    if int(ls) == le.id:
                        ll.departament += [le]

            #ll.departament={'asd': 'as'}
        return render(request, self.template, locals())

    def post(self, request, **kwargs):

        return render(request, self.template, locals())
