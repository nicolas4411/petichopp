from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('confirmar-senha/', views.confirmar_senha_financeiro, name='confirmar_senha'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('despesa/nova/', views.cadastrar_despesa, name='cadastrar_despesa'),
]