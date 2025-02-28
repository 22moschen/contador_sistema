from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from .models import SWOT, Empresa, RespostaFormulario, Relatorio, Formulario
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt  # Importando csrf_exempt

# Create your views here.

def home(request):
    return render(request, 'formulario/formulario.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'formulario/login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'formulario/login.html')

@csrf_exempt  # Permitir requisições GET e POST
def logout_view(request):    
    logout(request)
    return redirect('login')  # Redireciona para a página de login após o logout

def criar_formulario(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # Lógica para criar um novo formulário
        nome_formulario = request.POST.get('nome_formulario')
        # Salvar o formulário no banco de dados
        formulario = Formulario.objects.create(nome=nome_formulario, usuario=request.user)
        # Formulario.objects.create(nome=nome_formulario, ...)
        return JsonResponse({'status': 'success', 'message': 'Formulário criado com sucesso!'})
    return render(request, 'formulario/criar_formulario.html')


def exibir_formulario(request):
    if request.user.is_authenticated:
        return render(request, 'formulario/formulario.html')
    return redirect('login')


def compartilhar_formulario(request):
    if request.method == 'POST' and request.user.is_authenticated:
        email_cliente = request.POST.get('email_cliente')
        # Lógica para compartilhar o formulário com o cliente via email
        # Enviar email com o link do formulário
        send_mail(
            'Formulário Compartilhado',
            f'Você recebeu um formulário: {request.build_absolute_uri("/formulario/")}',
            'from@example.com',
            [email_cliente],
            fail_silently=False,
        )
        # Enviar email com o link do formulário
        return JsonResponse({'status': 'success', 'message': 'Formulário compartilhado com sucesso!'})

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

def responder_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        if resposta:
            RespostaFormulario.objects.create(
                formulario=formulario,
                resposta=resposta
            )
            return JsonResponse({'status': 'success', 'message': 'Resposta enviada com sucesso!'})
    return render(request, 'formulario/responder_formulario.html', {'formulario': formulario})

def exibir_swot_form(request):

    if request.user.is_authenticated:
        return render(request, 'formulario/swot_form.html')
    return redirect('login')


def submeter_swot_formulario(request):    
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Usuário não autenticado.'}, status=403)

    if request.method == 'POST':
        data = json.loads(request.body)
        empresa_id = data.get('empresa_id')
        empresa = get_object_or_404(Empresa, id=empresa_id)
        perguntas_respostas = data.get('perguntas_respostas')

        # Processar os dados SWOT
        cnpj = data.get('cnpj')
        forcas = data.get('forcas')
        fraquezas = data.get('fraquezas')
        oportunidades = data.get('oportunidades')
        ameacas = data.get('ameacas')

        perguntas_respostas = data.get('perguntas_respostas')

        # Processar os dados SWOT
        cnpj = data.get('cnpj')
        forcas = data.get('forcas')
        fraquezas = data.get('fraquezas')
        oportunidades = data.get('oportunidades')
        ameacas = data.get('ameacas')

        if cnpj and forcas and fraquezas and oportunidades and ameacas:
            swot = SWOT.objects.create(
                cnpj=cnpj,
                forcas=forcas,
                fraquezas=fraquezas,
                oportunidades=oportunidades,
                ameacas=ameacas
            )

            # Gerar relatório (exemplo simplificado)
            pontos_fortes = "Pontos fortes da empresa..."
            pontos_fracos = "Pontos fracos da empresa..."
            recomendacoes = "Cursos do Sebrae recomendados..."

            Relatorio.objects.create(
                empresa=empresa,
                pontos_fortes=pontos_fortes,
                pontos_fracos=pontos_fracos,
                recomendacoes=recomendacoes
            )

            return JsonResponse({'status': 'success', 'message': 'Formulário submetido com sucesso!'})
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)
