from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html, strip_tags

from documents.models import Document, Receiver, Remittent, Document_type, Alertmessage
from documents.forms import DocumentForm, RemittentForm, ReceiverForm
from django.utils.safestring import mark_safe
from authentication.models import Departament
from django.utils.dateparse import parse_date
import datetime, time
from dashboard import views
import  ast
from django.views import View


def Current_date():
    x = datetime.datetime.now()
    y = time.strftime("%A")

    def sw_dia(x):
        return {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miercoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sabado',
            'Sunday': 'Domingo',
        }[x]

    def sw_mes(x):
        return {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre',
        }[x]

    fecha = {
        'nday': sw_dia(y),
        'day': x.day,
        'month': sw_mes(x.month),
        'year': x.year
    }
    return fecha

def Document_create(request):
    depto= Departament.objects.get(id=request.session['departament']['active_id'])
    doc_for_dept= Document.objects.filter(departament=request.session['departament']['active_id'])
    date = Current_date()
    date_str = date['nday']+", "+str(date['day']) + " de " + date['month'] + " del " + str(date['year'])
    data = {}
    if request.method == 'POST':

        form = DocumentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.departament = depto
            valdos = 0
            if doc_for_dept.count() > 0:
                type = doc_for_dept.filter(type=obj.type)
                last_document = type.last()
                data['change'] = last_document.change
                obj.number = int(last_document.number) + 1
                if obj.remittent != last_document.remittent:
                    valdos = valdos + 1
                if obj.receiver != last_document.receiver:
                    valdos = valdos + 1
                if obj.body != last_document.body:
                    valdos = valdos + 1
                if obj.footer != last_document.footer:
                    valdos = valdos + 1
                if obj.matter != last_document.matter:
                    valdos = valdos + 1
                if obj.change != last_document.change:
                    valdos = valdos + 1
                if obj.previous != last_document.previous:
                    valdos = valdos + 1


                if valdos < 2:
                    act= Document.objects.get(id=last_document.id)
                    act.number=last_document.number
                    act.matter=obj.matter
                    act.remittent=obj.remittent
                    act.receiver=obj.receiver
                    act.body=obj.body
                    act.footer=obj.footer
                    act.previous=obj.previous
                    act.save()
                    obj.id = last_document.id
                    if valdos > 0:
                        request.session['alert']= 'Se a modificado el documento. '+ str(obj.id)
                else:

                    obj.year = date['year']
                    form.save()

            else:
                obj.number = 1

                #obj.creacion = date_str
                obj.year = date['year']
                obj.type_id = 1
                form.save()

            return redirect('document:documento_detalle', obj.id)
        else:
            print(form.is_valid())
            print(form.errors)
            form = DocumentForm(request.POST)

    else:
        form = DocumentForm()
    data['doc_for_dept'] = doc_for_dept
    data['edit']=True #Para activar texto enriquesido
    data['remittent'] = Remittent.objects.filter(active=True).order_by('id')
    data['receiver'] = Receiver.objects.filter(active=True).order_by('id')
    data['type'] = Document_type.objects.all().order_by('id')
    data['form']= form
    data['date']= date
    data['model']= doc_for_dept.last()
    print(data['model'].change)
    return render(request, 'document/form.html', data)

def Create_value(request, value):
    data = {'value': value}
    if value == 'remittent':
        data['titulo'] = 'Remitente'
        data['tema'] = 'remitente'
        if Remittent.objects.all().count() >= 1:
            data['model'] = Remittent.objects.filter(active=True).order_by('last_name')
        data['form'] = RemittentForm()
        if request.method == 'POST':
            data['form'] = RemittentForm(request.POST)
            if data['form'].is_valid():
                data['form'].save()
            return redirect('document:document_form')
    elif value == 'receiver':
        data['titulo'] = 'Receptor'
        data['tema'] = 'receptor'
        if Receiver.objects.all().count() >= 1:
            data['model'] = Receiver.objects.all().order_by('last_name')
        data['form'] = ReceiverForm()
        if request.method == 'POST':
            data['form'] = ReceiverForm(request.POST)
            if data['form'].is_valid():
                data['form'].save()
            return redirect('document:document_form' )

    return render(request, 'document/create_value.html', data)

def Edit_value(request, value, id_value):
    data = {'value': value}
    if value == 'remittent':
        data['titulo'] = 'Remitente'
        data['tema'] = 'remitente'
        data['edit'] = True  # Para activar texto enriquesido
        data['model'] = Remittent.objects.filter(active=True).order_by('first_name')
        data['modelform'] = Remittent.objects.get(id = id_value)
        if request.method == 'GET':
            data['form'] = RemittentForm(data['modelform'])

        else:
            data['form'] = RemittentForm(request.POST, instance=data['modelform'])

            if data['form'] .is_valid():
                data['form'].save()
            return redirect('document:document_form' )

    elif value == 'receiver':
        data['titulo'] = 'Receptor'
        data['tema'] = 'receptor'
        data['model'] = Receiver.objects.all().order_by('first_name')
        data['modelform'] = Receiver.objects.get(id=id_value)
        if request.method == 'GET':
            data['form'] = RemittentForm(instance=data['modelform'])
        else:
            data['form'] = ReceiverForm(request.POST, instance=data['modelform'])
            if data['form'] .is_valid():
                data['form'].save()
            return redirect('document:document_form' )

    return render(request, 'document/create_value.html', data)

def Active_off(request, **kwargs):
    print(kwargs)
    value = kwargs['value']
    id_value = kwargs['id_value']
    if value == 'remittent':
        value_ = Remittent.objects.get(id=id_value)
        value_.active = False
        value_.save()
        return redirect('document:create_value', value)
    elif value == 'receiver':
        value_ = Receiver.objects.get(id=id_value)
        value_.active = False
        value_.save()
        return redirect('document:create_value', value)
    elif value == 'documento':
        value_ = Document.objects.get(id=id_value)
        value_.active = False
        value_.save()
        return redirect('document:documento_list')

def Document_edit(request, id_documento):

    doc_for_dept= Document.objects.filter(departament=request.session['departament']['active_id'])
    data={'model' : Document.objects.get(id=id_documento)}
    if request.method == "GET":
        form = DocumentForm(instance=data['model'])
    else:
        form = DocumentForm(request.POST, instance=data['model'])
        print(form)
        if form.is_valid():
            form.save()
        else:
            print(form.is_valid())
            print(form.errors)
            form = DocumentForm(request.POST)
        return redirect('document:documento_list')
    date = Current_date()
    if Document.objects.filter(id=data['model'].previous).count()>0:
        data['previous'] = Document.objects.get(id=data['model'].previous)
    data['doc_for_dept'] = doc_for_dept
    data['remittent'] = Remittent.objects.filter(active=True).order_by('id')
    data['receiver'] = Receiver.objects.filter(active=True).order_by('id')
    data['type'] = Document_type.objects.all().order_by('id')
    data['form']= form
    data['date']= date
    data['editdoc']=True
    data['edit']=True
    return render(request, 'document/form.html', data)

def Document_list(request):
    model = Document.objects.filter(departament=request.session['departament']['active_id']).order_by('id')
    return render(request, 'document/list.html', {'model': model})

def Document_list_filter(request, **kwargs):
    model = Document.objects.filter(departament=request.session['departament']['active_id']).order_by('id')
    if kwargs['value']== 'null':
        model = Document.objects.filter(departament=request.session['departament']['active_id'], activo=False).order_by('id')
    elif kwargs['value'] == 'printed':
        model = Document.objects.filter(departament=request.session['departament']['active_id'], print=True).order_by('id')
    elif kwargs['value'] == 'pending':
        model = Document.objects.filter(departament=request.session['departament']['active_id'],activo=True, print=False).order_by('id')
    return render(request, 'document/list.html', {'model': model})

def Detalle_doc(request, id_docum, **kwargs):
    print(kwargs)
    data = {
        'detail': Document.objects.get(id=id_docum),
        'date': str(Document.objects.get(id=id_docum).created_at),
        'body' : mark_safe(Document.objects.get(id=id_docum).body),
        'signature' : mark_safe(Document.objects.get(id=id_docum).remittent.signature),
    }
    if Document.objects.filter(previous=Document.objects.get(id=id_docum).id).count()>0:
        data['previous']= Document.objects.get(previous=Document.objects.get(id=id_docum).id)
    if request.session['alert']:
        data['alert']=request.session['alert']
        request.session['alert']=None
    return render(request, "document/detail.html", data)

def Resumen(request, **kwargs):
    data = {}
    if Document.objects.filter(departament=request.session['departament']['active_id']):
        data['model'] = Document.objects.filter(departament=request.session['departament']['active_id']).order_by('-id')[:5]
    data['document_create'] =  Document.objects.filter(departament=request.session['departament']['active_id']).count()
    data['document_printed'] =  Document.objects.filter(departament=request.session['departament']['active_id'], print=True).count()
    data['document_pending'] =  Document.objects.filter(departament=request.session['departament']['active_id'], print=False, activo=True).count()
    data['document_null'] =  Document.objects.filter(departament=request.session['departament']['active_id'], activo=False).count()


    return render(request, 'document/resume.html', data)

def prints(request, **kwargs):

    obj = Document.objects.get(id=kwargs['id_docum'])
    obj.print = True
    obj.save()
    request.session['alert'] = 'printed'


    return redirect('document:documento_detalle', kwargs['id_docum'])

def getMessage(tipo):
    return Alertmessage.objects.get(tipo=tipo)

def setMessage(tipo, msj, id):
    obj = Alertmessage.objects.get(tipo=tipo)
    obj.message = msj
    obj.dueno = id
    obj

class ListPersonalized(View):
    template = 'document/personalized_list.html'

    def get(self, request):
        type = Document_type.objects.all()
        remittent = Remittent.objects.all()
        receiver = Receiver.objects.all()
        matter = Document.objects.filter(departament=request.session['departament']['active_id'],).order_by('matter')

        return render(request, self.template, locals())

class ListPersonalizedSet(View):
    template = 'document/personalized_list.html'


    def get(self, request, **kwargs):
        type = Document_type.objects.all()
        remittent= Remittent.objects.all()
        receiver = Receiver.objects.all()
        matter = Document.objects.filter(departament=request.session['departament']['active_id'],).order_by('matter')

        dere = kwargs['dere']
        date_ = kwargs['date']
        date = date_.replace('AND', '&')
        date = date.replace('_', '-')
        date_ = date.replace('-', '/')
        date_ = date_.replace('&', ' - ')
        date = date.split('&')
        null = False
        if kwargs['null']=='True':
            null = True
        type_ = None
        if kwargs['type'] != 'all':
            type_ = kwargs['type']
        else:
            type_ = None
        if Document_type.objects.filter(titulo=type_).count() >0:
            select_type = Document_type.objects.get(titulo=type_).titulo
            select_type_id = Document_type.objects.get(titulo=type_).id
        select_rem = []
        documents = []
        documents_ = []
        if kwargs['sere'] == 'remittent':
            dere = dere.replace('L','0')
            dere = dere.replace('0','')
            dere = dere.replace('Rrem_', '')
            dere = dere.replace('rem', ',')
            dere = dere.replace('_', '')
            dere = dere.split(',')
            for de in dere:
                select_rem += [de]
            for ll in dere:
                if ll:
                    if ll == 'all':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],)]
                    else:
                        documents_+=[Document.objects.filter(departament=request.session['departament']['active_id'],remittent=ll)]
        elif kwargs['sere'] == 'receiver':
            dere = dere.replace('L','')
            dere = dere.replace('Rrec_', '')
            dere = dere.replace('rec_', ',')
            dere = dere.replace('_', '')
            dere = dere.split(',')

            for ll in dere:
                if ll:
                    if ll == 'all':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],)]
                    else:
                        documents_+=[Document.objects.filter(departament=request.session['departament']['active_id'],receiver=ll)]
        elif kwargs['sere'] == 'matter':
            print('matter')
            dere = dere.replace('L','')
            dere = dere.replace('Rmat_', '')
            dere = dere.replace('mat_', ',')
            dere = dere.replace('_', '')
            dere = dere.split(',')

            for ll in dere:
                if ll:
                    if ll == 'all':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],)]
                    else:
                        documents_+=[Document.objects.filter(departament=request.session['departament']['active_id'],id=ll)]
        else:
            dere = dere.split('0')

            for ll in dere:
                ll = ll.replace('rem_', "'remitten' ,")
                ll = ll.replace('rec_', "'receiver' ,")
                ll = ll.replace('mat_', "'matter' ,")
                ll = ll.replace('L', ',')
                if ll =='all,':
                    documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],)]
                else:
                    ll = '['+ll+']'

                    ll = ast.literal_eval(ll)
                    if ll[0]== 'remitten':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],remittent_id=ll[1])]
                    elif ll[0] == 'receiver':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],receiver_id=ll[1])]
                    elif ll[0] == 'matter':
                        documents_ += [Document.objects.filter(departament=request.session['departament']['active_id'],id=ll[1])]
        val = True

        for ll in documents_:
            for lo in ll:
                for do in documents:
                    if lo == do:
                        val = False
                if null:
                    if lo.created_at.date() <= parse_date(date[1]) and lo.created_at.date() >= parse_date(date[0]) and val and str(lo.type) == str(type_):
                        documents += [lo]
                else:
                    if lo.created_at.date() <= parse_date(date[1]) and lo.created_at.date() >= parse_date(date[0]) and val and lo.activo != null  and str(lo.type) == str(type_):
                        documents += [lo]

        return render(request, self.template, locals())

"""
######################### test
from django.shortcuts import render

from templated_docs import fill_template
from templated_docs.http import FileResponse

class ExportView(View):
    def get(self, request, **kwargs):
        doc = Document.objects.get(id=kwargs['id_docum'])
        doctype = kwargs['format']
        exp = {
            'id': doc.id,
            'number': doc.number,
            'matter': doc.matter,
            'body': strip_tags(doc.body)
        }
        print(exp)
        filename = fill_template('document/OFICIO_template.odt', exp, output_format=doctype)
        visible_filename = str(doc.type)+' '+str(doc.number)+'.{}'.format(doctype)

        return FileResponse(filename, visible_filename)
"""