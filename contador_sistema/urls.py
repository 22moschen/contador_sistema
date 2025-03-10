"""
URL configuration for contador_sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView  # Importando a view para obter o token
from formulario.views import dashboard, login_view  # Importando a view do dashboard e a view de login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),  # Adicionando a URL de login
    path('dashboard/', dashboard, name='dashboard'),  # URL do dashboard

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint para obter o token JWT
    path('', include('formulario.urls')),  # Servindo a aplicação React na URL raiz
]
