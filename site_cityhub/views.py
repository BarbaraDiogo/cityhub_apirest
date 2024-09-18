from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, TypeEnergy, Progress
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import decimal
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

UserModel = get_user_model()

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(username=email, password=senha)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Usuário logado com sucesso.')
            return redirect('meu_progresso')
        else:
            messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'registration/login.html')

@login_required(login_url='/login/')
def area_logada(request):
    if request.user.is_authenticated:
        return render(request, 'registration/area_logada.html')
    else:
        return redirect('cadastro')

def sair(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('index')

def deletar_conta(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Conta deletada com sucesso.')
        return redirect('index')
    else:
        messages.error(request, 'Você precisa estar logado para deletar sua conta.')
        return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            user = UserModel.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            #user.save()
            messages.success(request, f"Usuário {email} registrado com sucesso.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Erro ao registrar usuário: {e}")
            return render(request, 'cadastro.html', {'error': str(e)})
    return render(request, 'cadastro.html')

def calcular_rank(porcentagem):
    if porcentagem >= 50:
        return "Amigo da Natureza"
    elif porcentagem >= 40:
        return "Guardião Verde"
    elif porcentagem >= 30:
        return "Defensor da Sustentabilidade"
    elif porcentagem >= 20:
        return "Protetor do Planeta"
    elif porcentagem >= 10:
        return "Amigo do Ambiente"
    else:
        return "Iniciante Ecológico"

@login_required(login_url='/login/')
def progresso(request):
    try:
        ultimo_progresso = Progress.objects.filter(user=request.user).latest('id')
        economia = ultimo_progresso.custoAnterior - ultimo_progresso.custoAtual
        
        if ultimo_progresso.custoAnterior > 0:
            porcentagem = (abs(economia) / ultimo_progresso.custoAnterior) * 100
            porcentagem = round(porcentagem)
            
            rank = calcular_rank(porcentagem)
            
            if economia < 0:
                titulo = 'Não houve economia:'
                mensagem_economia = f"acréscimo de R$ {abs(economia):.2f} este mês"
                mensagem_porcentagem = f"aumento de {porcentagem}%"
            else:
                titulo = 'Você economizou:'
                mensagem_economia = f"R$ {economia:.2f} este mês"
                mensagem_porcentagem = f"economia de {porcentagem}%"
        else:
            titulo = 'Custos não disponíveis'
            porcentagem = 0
            mensagem_economia = "R$ 0,00 este mês"
            mensagem_porcentagem = "economia de 0%"
            rank = "Sem dados suficientes"

        return render(request, 'progresso.html', {
            'titulo': titulo,
            'economia': mensagem_economia,
            'porcentagem': mensagem_porcentagem,
            'rank': rank
        })
    except Progress.DoesNotExist:
        return render(request, 'progresso.html', {
            'titulo': 'Sem dados de progresso',
            'economia': "R$ 0,00 este mês",
            'porcentagem': "economia de 0%",
            'rank': "Sem progresso registrado"
        })

def esqueci_senha(request):
    return render(request, 'esqueci_senha.html')

def meu_progresso(request):
    tipos_energia = TypeEnergy.objects.all()
    if request.method == 'POST':
        email_usuario = request.POST.get('email')
        energia_anterior_id = request.POST.get('tipo_energia_anterior')
        energia_atual_id = request.POST.get('tipo_energia_atual')
        custo_anterior = request.POST.get('custo_anterior')
        custo_atual = request.POST.get('custo_atual')
        duracao = request.POST.get('duracao')
        data = request.POST.get('data')

        try:
            user = UserModel.objects.get(email=email_usuario)  # Obter a instância do usuário
            tipo_energia_anterior = TypeEnergy.objects.get(id=energia_anterior_id)
            tipo_energia_atual = TypeEnergy.objects.get(id=energia_atual_id)

            progresso = Progress(
                user=user,  # Passando a instância correta do usuário
                energiaAnterior=tipo_energia_anterior,
                energiaAtual=tipo_energia_atual,
                custoAnterior=decimal.Decimal(custo_anterior),
                custoAtual=decimal.Decimal(custo_atual),
                duracao=decimal.Decimal(duracao),
                dt=data
            )
            progresso.save()
            messages.success(request, "Dados salvos com sucesso!")
            return redirect('progresso')

        except UserModel.DoesNotExist:
            messages.error(request, "Erro: Usuário não encontrado.")
        except ValidationError as e:
            messages.error(request, f"Erro de validação: {e}")
        except Exception as e:
            messages.error(request, f"Erro ao salvar os dados: {e}")
        return render(request, 'meu_progresso.html', {'tipos_energia': tipos_energia})
    else:
        return render(request, 'meu_progresso.html', {'tipos_energia': tipos_energia})
