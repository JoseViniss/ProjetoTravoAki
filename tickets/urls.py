from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('novo/', views.novo_chamado, name='novo_chamado'),
    path('pesquisar/', views.pesquisar_chamado, name='pesquisar_chamado'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tratar/<uuid:ticket_id>/', views.tratar_chamado, name='tratar_chamado'),
    path('cadastro/', views.cadastro_tecnico, name='cadastro'),
]