from django.shortcuts import render, redirect
from .models import Req
from django.contrib.auth.models import User
from authentication.models import Logeado
from department.models import Departament
from django.views import View

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
        for re in req:
           re.admin_icon = self.icon(re.admin)
           re.tick_icon = self.icon(re.tick)
           re.docs_icon = self.icon(re.docs)


        users = Logeado.objects.all()
        dep = Departament.objects.all()
        lo = None
        for ll in req:
            ll.dpts_str=str(ll.dpts)
            lo = str(ll.dpts)
            lo = lo.split('d')
            lo = lo.split(',')
            ll.dpts = []
            for ls in lo:
                for le in dep:
                    if int(ls) == le.id:
                        ll.dpts += [le]
        for ll in users:
            if ll.departament != ',':
                lo = ll.departament
            lo = lo.split('d')
            lo = lo.split(',')
            ll.departament = []
            for ls in lo:
                for le in dep:
                    if int(ls) == le.id:
                        ll.departament += [le]
        return render(request, self.template, locals())

class Register(View):

    def get(self, request, **kwargs):
        req = Req.objects.get(id=kwargs['id'])
        req.active = False
        req.save()
        loge = Logeado.objects.get(user_id=req.user.user.id)
        loge.tick = kwargs['tick']
        loge.admin = kwargs['admin']
        loge.docs = kwargs['docs']
        loge.departament = kwargs['dpts']
        loge.new = False
        loge.save()
        return redirect('administrator:select')


import xlwt

from django.http import HttpResponse

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First name', 'Last name', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response