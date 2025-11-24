from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TicketForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Ticket, Interacao
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TicketForm, EditarTicketForm, InteracaoForm
import uuid
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def novo_chamado(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            
            return render(request, 'tickets/sucesso.html', {'ticket': ticket})
    else:
        form = TicketForm()

    return render(request, 'tickets/novo_chamado.html', {'form': form})

def index(request):
    """Página inicial do sistema"""
    return render(request, 'tickets/index.html')

def pesquisar_chamado(request):
    query = request.GET.get('protocolo', '').strip()
    
    if not query:
        return render(request, 'tickets/index.html', {'erro': 'Por favor, digite um código ou nome.'})

    filtros = Q(nome_solicitante__icontains=query) | Q(empresa__icontains=query)

    try:
        uuid_obj = uuid.UUID(query)
        filtros |= Q(ticket_id=uuid_obj)
    except (ValueError, ValidationError):
        pass

    resultados = Ticket.objects.filter(filtros)
    
    if not resultados.exists():
        return render(request, 'tickets/index.html', {
            'erro': f'Nenhum chamado encontrado para "{query}".'
        })

    if resultados.count() == 1:
        return render(request, 'tickets/acompanhar_chamado.html', {'ticket': resultados.first()})

    return render(request, 'tickets/lista_publica.html', {'tickets': resultados, 'termo': query})

@login_required
def dashboard(request):
    filtro = request.GET.get('filtro', 'todos')
    query = request.GET.get('q') # Pega o termo digitado na busca
    
    # Começa com todos
    tickets = Ticket.objects.all()

    # 1. Aplica a BUSCA TEXTUAL (Se houver)
    if query:
        tickets = tickets.filter(
            Q(nome_solicitante__icontains=query) | 
            Q(empresa__icontains=query) |
            Q(descricao__icontains=query) |
            Q(ticket_id__icontains=query) # Bônus: busca por pedaço do ID
        )

    # 2. Aplica os FILTROS de Status (Lógica existente...)
    if filtro == 'meus':
        tickets = tickets.filter(tecnico=request.user).exclude(status='resolvido')
    elif filtro == 'outros':
        tickets = tickets.exclude(tecnico=request.user).exclude(tecnico__isnull=True).exclude(status='resolvido')
    elif filtro == 'fechados':
        tickets = tickets.filter(status='resolvido')
    else:
        tickets = tickets.exclude(status='resolvido')

    # Bônus: Pequena Estatística para o Requisito 3
    total_abertos = Ticket.objects.exclude(status='resolvido').count()

    return render(request, 'tickets/dashboard.html', {
        'tickets': tickets, 
        'filtro_atual': filtro,
        'total_abertos': total_abertos # Passando a estatística
    })

@login_required
def tratar_chamado(request, ticket_id):
    # Busca o ticket pelo UUID
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    
    form_status = EditarTicketForm(instance=ticket)
    form_interacao = InteracaoForm()

    if request.method == 'POST':
        # Verifica se é uma atualização de STATUS
        if 'btn_status' in request.POST:
            form_status = EditarTicketForm(request.POST, instance=ticket)
            if form_status.is_valid():
                form_status.save()
                return redirect('tratar_chamado', ticket_id=ticket.ticket_id)

        # Verifica se é uma nova MENSAGEM
        elif 'btn_mensagem' in request.POST:
            form_interacao = InteracaoForm(request.POST)
            if form_interacao.is_valid():
                interacao = form_interacao.save(commit=False)
                interacao.ticket = ticket
                interacao.autor = request.user
                interacao.save()
                return redirect('tratar_chamado', ticket_id=ticket.ticket_id)

    return render(request, 'tickets/tratar_chamado.html', {
        'ticket': ticket,
        'form_status': form_status,
        'form_interacao': form_interacao
    })
    
def cadastro_tecnico(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: Já logar a pessoa direto após criar a conta
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/cadastro.html', {'form': form})