from django import forms
from .models import Ticket, Interacao

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome_solicitante', 'empresa', 'contato', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva seu problema com detalhes...'}),
        }

class EditarTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'tecnico']

class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva uma resposta interna ou para o cliente...'}),
        }