from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from financeiro.models import Transacao
from .models import Atendimento, Pet, Servico


# --- CONTA E SEGURANÇA ---

@login_required(login_url='login')
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('alterar_senha')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'petis/alterar_senha.html', {'form': form})


@staff_member_required(login_url='login')
def cadastrar_administrador(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email', '')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.success(request, f'Administrador {first_name} criado com sucesso!')
            return redirect('cadastrar_administrador')

    administradores = User.objects.filter(is_staff=True)
    return render(request, 'petis/cadastrar_administrador.html', {'administradores': administradores})


@staff_member_required(login_url='login')
def cadastrar_funcionario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                password=password
            )
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, f'Funcionário {first_name} cadastrado com sucesso!')
            return redirect('cadastrar_funcionario')

    funcionarios = User.objects.filter(is_staff=False)
    return render(request, 'petis/cadastrar_funcionario.html', {'funcionarios': funcionarios})


# --- AUTENTICAÇÃO ---

def user_login(request):
    if request.user.is_authenticated:
        return redirect('visualizar_petis')

    erro = None
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")

        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'visualizar_petis')
            return redirect(next_url)
        else:
            erro = "Usuário ou senha inválidos."

    return render(request, 'login.html', {'erro': erro})


def user_logout(request):
    logout(request)
    return redirect('login')


# --- GESTÃO DE PETS ---

@login_required(login_url='login')
def cadastrar_pet(request):
    erro = None
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        especie = request.POST.get("especie", "").strip()
        raca = request.POST.get("raca", "").strip()
        idade = request.POST.get("idade", "").strip()
        dono = request.POST.get("dono", "").strip()
        telefone_dono = request.POST.get("telefone_dono", "").strip()

        if nome and especie and raca and idade and dono and telefone_dono:
            pet_existente = Pet.objects.filter(nome__iexact=nome, dono__iexact=dono).first()

            if pet_existente:
                status_texto = "Ativo" if pet_existente.ativo else "Inativo"
                erro = f"Já existe um pet cadastrado com o nome '{nome}' para o tutor '{dono}' (Status atual: {status_texto})."
                return render(request, 'cadastrar_pet.html', {
                    'erro': erro,
                    'pet_existente': pet_existente,
                    'form_data': request.POST
                })

            Pet.objects.create(
                nome=nome,
                especie=especie,
                raca=raca,
                idade=idade,
                dono=dono,
                telefone_dono=telefone_dono,
                ativo=True
            )
            return redirect('visualizar_petis')

    return render(request, 'cadastrar_pet.html')


@login_required(login_url='login')
def visualizar_petis(request):
    pets = Pet.objects.filter(ativo=True)
    return render(request, 'visualizar_petis.html', {'pets': pets})


@login_required(login_url='login')
def editar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == "POST":
        pet.nome = request.POST.get("nome")
        pet.especie = request.POST.get("especie")
        pet.raca = request.POST.get("raca")
        pet.idade = request.POST.get("idade")
        pet.dono = request.POST.get("dono")
        pet.telefone_dono = request.POST.get("telefone_dono")
        pet.save()
        return redirect('visualizar_petis')

    return render(request, 'editar_pet.html', {'pet': pet})


@login_required(login_url='login')
def alternar_status_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.ativo = not pet.ativo
    pet.save()
    return redirect('visualizar_petis')


@login_required(login_url='login')
def deletar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return redirect('visualizar_petis')


# --- CATÁLOGO DE SERVIÇOS ---

@login_required(login_url='login')
def gerenciar_servicos(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        preco = request.POST.get("preco", "").strip()
        if nome and preco:
            Servico.objects.create(nome=nome, preco_padrao=preco)
            return redirect('gerenciar_servicos')

    servicos = Servico.objects.all().order_by('nome')
    return render(request, 'gerenciar_servicos.html', {'servicos': servicos})


@login_required(login_url='login')
def deletar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    servico.delete()
    return redirect('gerenciar_servicos')


# --- ATENDIMENTOS ---

@login_required(login_url='login')
def novo_atendimento(request):
    pets = Pet.objects.filter(ativo=True)
    servicos = Servico.objects.all().order_by('nome')

    if request.method == "POST":
        pet_id = request.POST.get("pet")
        data_atendimento = request.POST.get("data")
        servicos_descricao = request.POST.get("servicos_descricao")
        valor_bruto = Decimal(request.POST.get("valor_total", "0") or "0")
        desconto_pct = Decimal(request.POST.get("desconto", "0") or "0")
        forma_pagamento = request.POST.get("forma_pagamento", "PIX")
        observacoes = request.POST.get("observacoes")

        # Aplica o desconto percentual mantendo tipo Decimal
        valor_desconto = valor_bruto * (desconto_pct / Decimal('100.0'))
        valor_final = max(Decimal('0.00'), valor_bruto - valor_desconto)

        if pet_id and data_atendimento and valor_bruto:
            pet = get_object_or_404(Pet, id=pet_id)
            
            # 1. Registra no app petis
            atendimento = Atendimento.objects.create(
                pet=pet,
                data=data_atendimento,
                servicos_descricao=servicos_descricao,
                valor_total=valor_final,
                observacoes=observacoes,
                vendedor=request.user
            )

            # 2. Registra no app financeiro
            Transacao.objects.create(
                descricao=f"Atendimento: {pet.nome} ({servicos_descricao})",
                valor=valor_final,
                tipo='ENTRADA',
                forma_pagamento=forma_pagamento,
                data=data_atendimento,
                atendimento=atendimento,
                vendedor=request.user
            )

            return redirect('historico_atendimentos')

    return render(request, 'novo_atendimento.html', {
        'pets': pets,
        'servicos': servicos
    })


@login_required(login_url='login')
def historico_atendimentos(request):
    atendimentos = Atendimento.objects.select_related('pet', 'vendedor').order_by('-data', '-id')
    return render(request, 'historico_atendimentos.html', {'atendimentos': atendimentos})