from django.db import models
from django.contrib.auth.models import User
import uuid

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('aguardando', 'Aguardando Resposta'),
        ('respondido', 'Respondido'),
        ('em_progresso', 'Em Progresso'),
        ('em_espera', 'Em Espera'),
        ('resolvido', 'Resolvido'),
    ]

    # Identificação
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Protocolo")
    
    # Dados do Solicitante
    nome_solicitante = models.CharField(max_length=100, verbose_name="Nome")
    empresa = models.CharField(max_length=100)
    contato = models.CharField(max_length=100, verbose_name="Contato (Email/Tel)")
    descricao = models.TextField(verbose_name="Descrição do Problema")
    
    # Controle Interno
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    
    # Datas (Auto_now_add grava a data na criação, Auto_now atualiza a cada save)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Aberto em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última atualização")

    def __str__(self):
        return f"#{str(self.ticket_id)[:8]} - {self.nome_solicitante}"

    class Meta:
        ordering = ['-created_at'] # Padrão: mostra os mais recentes primeiro


class Interacao(models.Model):
    """
    Tabela para guardar o histórico de mensagens dentro do ticket
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='interacoes')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg em {self.ticket}"