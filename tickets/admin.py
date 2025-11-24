from django.contrib import admin
from .models import Ticket, Interacao

class InteracaoInline(admin.TabularInline):
    """Permite ver as mensagens DENTRO da tela do Ticket no admin"""
    model = Interacao
    extra = 0 # Não mostra linhas vazias extras

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id_curto', 'nome_solicitante', 'empresa', 'status', 'tecnico', 'created_at')
    list_filter = ('status', 'empresa', 'tecnico')
    search_fields = ('nome_solicitante', 'descricao', 'ticket_id')
    inlines = [InteracaoInline] # Adiciona as mensagens aqui dentro

    def ticket_id_curto(self, obj):
        return str(obj.ticket_id)[:8]
    ticket_id_curto.short_description = 'Protocolo'