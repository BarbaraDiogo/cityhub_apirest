"""
URL configuration for cityhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from site_cityhub import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('sobre', views.sobre, name='sobre'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('progresso', views.progresso, name='progresso'),
    path('esqueci_senha', views.esqueci_senha, name='esqueci_senha'),
    path('meu_progresso', views.meu_progresso, name='meu_progresso'),
    path('area_logada',views.area_logada, name='area_logada'),
    path('sair', views.sair, name='sair'),
    path('deletar_conta', views.deletar_conta, name='deletar_conta'),
] 
# adicionar essas duas linhas ao final que definem as rotas 
# de arquivo estaticos e de mídia
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
