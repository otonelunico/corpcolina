from django.shortcuts import render, redirect
from .forms import EstablecimientoForm, RespuestaForm, TicketForm, TemaForm, SegumentForm
from django.views import View
from .models import Tema, Establecimiento, Tecnico, Estado, Ticket, Respuestas
from django.utils.safestring import mark_safe
from authentication.models import Logeado
from authentication.views import userAdmin


template_no_valid = 'admin/error.html'

class State(View):
    template = 'ticket/states.html'

    def get(self, request):

        return render(request, self.template, locals())

class NewTicket(View):
    template = 'ticket/form.html'

    def get(self, request, *args, **kwargs):

        topics = Tema.objects.all()
        establishments = Establecimiento.objects.all()
        technicians = Tecnico.objects.all()
        states = Estado.objects.all()
        form = TicketForm()
        return render(request, self.template, locals())

    def post(self, request, **kwargs):
        form = TicketForm(request.POST)
        obj=None
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario = request.user
            form.save()
        return redirect('ticket:detail', obj.id )

class NewData(View):
    template = 'ticket/create.html'
    def get(self, request, *args, **kwargs):
        if kwargs['value']== 'topic':
            name = 'Tema'
            form = TemaForm()
        elif kwargs['value'] == 'establishment':
            name = 'Establecimiento'
            form = EstablecimientoForm()
        elif kwargs['value'] == 'technician':
            name = 'Tecnico'
            form = TecnicoForm()
        return render(request, self.template, locals())

    def post(self, request, **kwargs):
        form = None
        if kwargs['value']== 'topic':
            form = TemaForm(request.POST)
        elif kwargs['value'] == 'establishment':
            form = EstablecimientoForm(request.POST)
        elif kwargs['value'] == 'technician':
            form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()

        return render(request, self.template, locals())

class DetailTicket(View):
    template = 'ticket/detail.html'

    def get(self, request, *args, **kwargs):
        detalle = Ticket.objects.get(id = kwargs['id'])
        if detalle.asignado == request.session['id']:
            user_asign = True
        print(detalle.usuario.username)
        resp = Respuestas.objects.filter(ticket_id=detalle)
        detalle.detall_problema = mark_safe(detalle.detall_problema)
        for foo in resp:
            foo.mensaje = mark_safe(foo.mensaje)
        form = RespuestaForm()

        if detalle.asignado == None:
            detalle.asignado = 'A espera de asignacion de tecnico'
        else:
            detalle.asignado = Tecnico.objects.get(tecnico_id=detalle.asignado)

        print(request.session['id'])
        return render(request, self.template, locals())

    def post(self, request, **kwargs):
        detalle = Ticket.objects.get(id = kwargs['id'])
        resp = Respuestas.objects.filter(ticket_id=detalle)
        detalle.detall_problema = mark_safe(detalle.detall_problema)
        for foo in resp:
            foo.mensaje = mark_safe(foo.mensaje)
        form = RespuestaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario_id = request.session['id']
            obj.ticket = Ticket.objects.get(id = kwargs['id'])
            form.save()
        else:
            print(form.is_valid())
            print(form.errors)
        return redirect('ticket:detail', kwargs['id'])

class ListTicket(View):
    template = 'ticket/list.html'

    def get(self, request):
        tickets = Ticket.objects.filter(usuario=request.user).order_by('id')
        return render(request, self.template, locals())

class AllListTicket(View):
    template = 'ticket/list.html'

    def get(self, request):
        if userAdmin(request)!= True:
            return render(request, template_no_valid)
        tickets = Ticket.objects.all().order_by('id')
        return render(request, self.template, locals())

class Seguiment(View):
    template = 'ticket/segiment.html'

    def get(self, request, *args, **kwargs):
        form = SegumentForm()
        return render(request, self.template, locals())

    def post(self, request, **kwargs):
        error = None
        form = SegumentForm(request.POST)
        if form.is_valid():
            ticket = form.cleaned_data['codigo']
            if Ticket.objects.filter(id=ticket).count()>0:
                return redirect('ticket:detail', ticket)
            else:
                error= "Ticket solicitado no existe"
        return render(request, self.template, locals())