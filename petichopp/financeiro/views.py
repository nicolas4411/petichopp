import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum
from .models import Transacao

@staff_member_required(login_url='login')
def confirmar_senha_financeiro(request):
    """Exige confirmação de senha do administrador antes de acessar o financeiro."""
    if request.method == 'POST':
        senha = request.POST.get('senha')
        user = authenticate(username=request.user.username, password=senha)
        
        if user is not None and user.is_staff:
            request.session['financeiro_autorizado'] = True
            return redirect('financeiro:dashboard')
        else:
            messages.error(request, 'Senha incorreta!')

    return render(request, 'financeiro/confirmar_senha.html')


@staff_member_required(login_url='login')
def dashboard(request):
    """Painel Financeiro sem nenhuma comparação lógica dentro do HTML."""
    if not request.session.get('financeiro_autorizado', False):
        return redirect('financeiro:confirmar_senha')

    hoje = datetime.date.today()
    mes_selecionado = request.GET.get('mes', str(hoje.month))
    ano_selecionado = request.GET.get('ano', str(hoje.year))

    transacoes = Transacao.objects.select_related('vendedor').all()

    if mes_selecionado and mes_selecionado != 'todos':
        transacoes = transacoes.filter(data__month=int(mes_selecionado))
    if ano_selecionado and ano_selecionado != 'todos':
        transacoes = transacoes.filter(data__year=int(ano_selecionado))

    transacoes = transacoes.order_by('-data', '-id')

    total_entradas = transacoes.filter(tipo='ENTRADA').aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    total_saidas = transacoes.filter(tipo='SAIDA').aggregate(Sum('valor'))['valor__sum'] or Decimal('0.00')
    saldo_atual = total_entradas - total_saidas

    # Prepara os meses e resolve o estado 'selected' no próprio Python
    meses_brutos = [
        ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'),
        ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'),
        ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')
    ]
    meses_lista = [
        {
            'num': num,
            'nome': nome,
            'selected': (mes_selecionado == num)
        }
        for num, nome in meses_brutos
    ]

    # Prepara os anos e resolve o estado 'selected' no próprio Python
    anos_lista = [
        {
            'ano': str(ano),
            'selected': (ano_selecionado == str(ano))
        }
        for ano in range(hoje.year, hoje.year - 5, -1)
    ]

    return render(request, 'financeiro/dashboard.html', {
        'transacoes': transacoes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_atual': saldo_atual,
        'todos_meses_selecionado': (mes_selecionado == 'todos'),
        'todos_anos_selecionado': (ano_selecionado == 'todos'),
        'anos_lista': anos_lista,
        'meses_lista': meses_lista,
    })


@staff_member_required(login_url='login')
def cadastrar_despesa(request):
    """View para registrar saídas/gastos manuais no caixa."""
    if not request.session.get('financeiro_autorizado', False):
        return redirect('financeiro:confirmar_senha')

    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        valor = Decimal(request.POST.get('valor', '0') or '0')
        forma_pagamento = request.POST.get('forma_pagamento', 'PIX')
        data = request.POST.get('data')

        if descricao and valor > 0 and data:
            Transacao.objects.create(
                descricao=f"Gasto: {descricao}",
                valor=valor,
                tipo='SAIDA',
                forma_pagamento=forma_pagamento,
                data=data,
                vendedor=request.user
            )
            messages.success(request, 'Despesa/Gasto lançado com sucesso!')
            return redirect('financeiro:dashboard')
        else:
            messages.error(request, 'Preencha todos os campos corretamente.')

    return render(request, 'financeiro/cadastrar_despesa.html')