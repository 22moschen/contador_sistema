from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Formulario, Pergunta, Resposta, SWOTResponse, RespostaFormulario
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .forms import SWOTForm, PerguntaForm, RespostaForm


@login_required
def dashboard(request):
    # Dados para cards
    total_formularios = Formulario.objects.filter(contador=request.user).count()

    # Dados para o gráfico (ultimos 7 dias)
    date_range = [timezone.now() - timedelta(days=i) for i in range(6, -1, -1)]

    contagens_respostas = []
    datas_respostas = []

    for date in date_range:
        count = Resposta.objects.filter(
            formulario__contador=request.user,
            data_resposta__date=date.date()
        ).count()
        contagens_respostas.append(count)
        datas_respostas.append(date.strftime("%d/%m"))

    # Formularios recentes
    formularios = Formulario.objects.filter(
        contador=request.user,
    ).annotate(
        total_respostas=Count('resposta')
    ).order_by('-data_criacao')[:5]

    context = {
        'total_formularios': total_formularios,
        'contagens_respostas': contagens_respostas, 
        'datas_respostas': datas_respostas,
        'formularios': formularios
    }

    return render(request, 'formulario/dashboard.html', context)

def login_view(request):  # View para autenticação de usuários
    next_url = request.GET.get('next', '') #captura o parâmetro 'next' da URL

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', '') #captura do formulário
        try:
            user = User.objects.get(email=email) # Obtenha o usuário pelo e-mail
            auth_user = authenticate(
                request, 
                username=user.username,
                password=password 
            ) # Autenticação do usuário

            if auth_user is not None:
                login(request, auth_user) # Login do usuário
                return redirect(next_url if next_url else reverse('dashboard'))
            messages.error(request, 'Senha incorreta')
        except Exception as e:
            messages.error(request, f'Erro no login {str(e)}')
    return render(request, 'formulario/login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect(reverse('login') + '?next=' + request.GET.get('next', reverse('login')))

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Conta criada com sucesso! Você pode fazer login agora.')
        return redirect('login')
    return render(request, 'formulario/register_view.html')  

@login_required
def criar_formulario(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        formulario = Formulario.objects.create(
            titulo=titulo,
            contador=request.user
        )
        return redirect('editar_formulario', formulario_id=formulario.id)
    formularios = Formulario.objects.filter(contador=request.user)
    return render(request, 'formulario/criar_formulario.html', {'formularios': formularios})

@login_required
def editar_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id, contador=request.user)
    # Implementar lógica de edição de perguntas
    return render(request, 'formulario/editar_formulario.html', {
        'formulario': formulario
    })

@login_required
def exibir_swot_form(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    
    if request.method == 'POST':
        # Criar análise SWOT
        SWOTResponse.objects.create(
            formulario=formulario,
            strengths=request.POST.get('strengths'),
            weaknesses=request.POST.get('weaknesses'),
            opportunities=request.POST.get('opportunities'),
            threats=request.POST.get('threats')
        )
        messages.success(request, 'Análise SWOT salva com sucesso!')
        return redirect('detalhes_formulario', formulario_id=formulario.id)
    
    return render(request, 'formulario/swot_form.html', {
        'formulario': formulario
    })

@login_required
def responder_formulario(request, link_unico):
    # Implementar lógica para responder ao formulário usando o link único
    return render(request, 'formulario/responder_formulario.html', {
        'link_unico': link_unico
    })

@login_required
def compartilhar_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id, contador=request.user)
    # Implementar lógica de geração de link único
    return render(request, 'formulario/compartilhar.html', {
        'formulario': formulario
    })

@login_required
def analise_swot(request):
    # Implemente a lógica de análise SWOT global aqui
    swot_data = {
        'forcas': Resposta.objects.filter(tipo='F').count(),
        'fraquezas': Resposta.objects.filter(tipo='W').count(),
        'oportunidades': Resposta.objects.filter(tipo='O').count(),
        'ameacas': Resposta.objects.filter(tipo='A').count()
    }
    
    return render(request, 'formulario/analise_swot.html', {
        'swot_data': swot_data
    })

@login_required
def detalhes_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id, contador=request.user)
    return render(request, 'formulario/detalhes_formulario.html', {
        'formulario': formulario
    })