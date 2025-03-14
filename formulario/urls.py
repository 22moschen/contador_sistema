from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register_view'),
    path('analise-swot/', views.analise_swot, name='analise_swot'),  # NOVO
    path('formularios/<int:formulario_id>/swot/', views.exibir_swot_form, name='swot_form'),
     path('formularios/<int:formulario_id>/', views.detalhes_formulario, name='detalhes_formulario'),

    path('formularios/novo/', views.criar_formulario, name='criar_formulario'),
    path('formularios/<int:formulario_id>/editar/', views.editar_formulario, name='editar_formulario'),
    path('formularios/<int:formulario_id>/swot/', views.exibir_swot_form, name='swot_form'),
    path('formularios/<int:formulario_id>/compartilhar/', views.compartilhar_formulario, name='compartilhar_formulario'),
    
    path('responder/<uuid:link_unico>/', views.responder_formulario, name='responder_formulario'),
]