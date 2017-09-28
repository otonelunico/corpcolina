from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse_lazy
from documents.models import Document, Receiver, Remittent, Document_type, Alertmessage
from documents.forms import DocumentForm, RemittentForm, ReceiverForm
from django.utils.safestring import mark_safe
from authentication.models import Departament
import datetime, time
from dashboard import views

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
                print(last_document.number)
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


                if valdos < 2:
                    act= Document.objects.get(id=last_document.id)
                    act.number=last_document.number
                    act.matter=obj.matter
                    act.remittent=obj.remittent
                    act.receiver=obj.receiver
                    act.body=obj.body
                    act.footer=obj.footer
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

    data['edit']=True #Para activar texto enriquesido
    data['remittent'] = Remittent.objects.filter(active=True).order_by('id')
    data['receiver'] = Receiver.objects.filter(active=True).order_by('id')
    data['type'] = Document_type.objects.all().order_by('id')
    data['form']= form
    data['date']= date
    data['model']= doc_for_dept.last()
    return render(request, 'document/form.html', data)

def Create_value(request, value):
    data = {'value': value}
    if value == 'remittent':
        data['titulo'] = 'Remitente'
        data['tema'] = 'remitente'
        if Remittent.objects.all().count() >= 1:
            data['model'] = Remittent.objects.all().order_by('last_name')
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
        data['model'] = Remittent.objects.all().order_by('first_name')
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

def Active_off(request, value, id_value):
    if value == 'desde':
        value_ = Remittent.objects.get(id=id_value)
        value_.activo = False
        value_.save()
        return redirect('document:create_value', value)
    elif value == 'para':
        value_ = Receiver.objects.get(id=id_value)
        value_.activo = False
        value_.save()
        return redirect('document:create_value', value)
    elif value == 'documento':
        value_ = Document.objects.get(id=id_value)
        value_.activo = False
        value_.save()
        return redirect('document:documento_list')

def Document_edit(request, id_documento):

    data={'model' : Document.objects.get(id=id_documento)}
    if request.method == "GET":
        form = DocumentForm(instance=data['model'])
    else:
        form = DocumentForm(request.POST, instance=data['model'])
        if form.is_valid():
            form.save()
        return redirect('document:documento_list')
    date = Current_date()
    data['remittent'] = Remittent.objects.filter(active=True).order_by('id')
    data['receiver'] = Receiver.objects.filter(active=True).order_by('id')
    data['type'] = Document_type.objects.all().order_by('id')
    data['form']= form
    data['date']= date
    data['editdoc']=True
    data['edit']=True
    print(data['model'].change)
    return render(request, 'document/form.html', data)

def Document_list(request):
    model = Document.objects.filter(departament=request.session['departament']['active_id']).order_by('id')
    return render(request, 'document/list.html', {'model': model})

def Detalle_doc(request, id_docum):
    marker='<style> .marker {background-color: yellow;}</style>'
    data = {
        'detail': Document.objects.get(id=id_docum),
        'date': str(Document.objects.get(id=id_docum).created_at),
        'body' : mark_safe(marker+' '+Document.objects.get(id=id_docum).body),
        'signature' : mark_safe(marker+' '+Document.objects.get(id=id_docum).remittent.signature),
    }
    print(Document.objects.get(id=id_docum).created_at)
    if request.session['alert']:
        data['alert']=request.session['alert']
        request.session['alert']=None
    print(data)
    return render(request, "document/detail.html", data)

def Resumen(request, **kwargs):
    data = {}
    if Document.objects.filter(departament=request.session['departament']['active_id']):
        data['model'] = Document.objects.filter(departament=request.session['departament']['active_id']).order_by('id')[:5]
    data['document_create'] =  Document.objects.filter(departament=request.session['departament']['active_id']).count()

    return render(request, 'document/resume.html', data)

def getMessage(tipo):
    return Alertmessage.objects.get(tipo=tipo)

def setMessage(tipo, msj, id):
    obj = Alertmessage.objects.get(tipo=tipo)
    obj.message = msj
    obj.dueno = id
    obj