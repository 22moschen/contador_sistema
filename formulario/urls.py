from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [  
    path('swot/', views.exibir_swot_form, name='exibir_swot_form'),  # Rota para exibir o formulário SWOT
    path('submeter_swot/', views.submeter_swot_formulario, name='submeter_swot_formulario'),  # Rota para submeter o formulário SWOT

    path('', views.home, name='home'),  # Rota para a página inicial
    path('formulario/', views.exibir_formulario, name='exibir_formulario'),  # Rota para exibir o formulário
    path('submeter/', views.submeter_swot_formulario, name='submeter_formulario'),    
    path('login/', views.login_view, name='login'),  # Rota para login
    path('logout/', views.logout_view, name='logout'),  # Rota para logout usando nossa view personalizada
    path('criar/', views.criar_formulario, name='criar_formulario'),  # Rota para criar formulário
    path('compartilhar/', views.compartilhar_formulario, name='compartilhar_formulario'),  # Rota para compartilhar formulário
    path('responder/<int:formulario_id>/', views.responder_formulario, name='responder_formulario'),  # Rota para responder a um formulário
]