from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Formulario, Pergunta, Resposta, SWOTResponse, RespostaFormulario
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
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
            Formulario__contador=request.user,
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
        'contagens_respostas': mark_safe(serialize('json', contagens_respostas)), 
        'datas_respostas': mark_safe(serialize('json', datas_respostas)),
        'formularios': formularios
    }

    return render(request, 'dashboard.html', context)

def login_view(request):  # View para autenticação de usuários
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Usuário ou senha inválidos.')  # Adicionando mensagem de erro
    return render(request, 'formulario/login.html')  # Retorna a página de login

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def criar_formulario(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        formulario = Formulario.objects.create(
            titulo=titulo,
            contador=request.user
        )
        return redirect('editar_formulario', formulario_id=formulario.id)
    return render(request, 'formulario/criar_formulario.html')

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
        form = SWOTForm(request.POST)
        if form.is_valid():
            SWOTResponse.objects.create(
                formulario=formulario,
                **form.cleaned_data
            )
            return redirect('detalhes_formulario', formulario_id=formulario.id)
    
    form = SWOTForm()
    
    return render(request, 'formulario/swot_form.html', {
        'form': form,
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
