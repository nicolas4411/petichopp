from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizar_petis, name='visualizar_petis'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cadastrar/', views.cadastrar_pet, name='cadastrar_pet'),
    path('editar/<int:pet_id>/', views.editar_pet, name='editar_pet'),
    path('status/<int:pet_id>/', views.alternar_status_pet, name='alternar_status_pet'),
    path('deletar/<int:pet_id>/', views.deletar_pet, name='deletar_pet'),
    path('servicos/', views.gerenciar_servicos, name='gerenciar_servicos'),
    path('servicos/deletar/<int:servico_id>/', views.deletar_servico, name='deletar_servico'),
    path('atendimentos/novo/', views.novo_atendimento, name='novo_atendimento'),
    path('atendimentos/historico/', views.historico_atendimentos, name='historico_atendimentos'),
    path('funcionarios/cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('administradores/cadastrar/', views.cadastrar_administrador, name='cadastrar_administrador'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
]