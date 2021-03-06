"""desapegalivro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from . import views

app_name='core'

urlpatterns = [
    path('', views.Home.as_view(),name='home'),
    path('cadastro_livro/', views.CadastroLivro.as_view(),name='cadastro_livro'),
    path('detalhe_livro/<int:livro_id>', views.DetalheLivro.as_view(),name='detalhe_livro'),
    path('adquirir_livro/<int:livro_id>', views.AdquirirLivro.as_view(),name='adquirir_livro'),
    path('livro_requisitados/', views.LivrosRequisitados.as_view(),name='livros_requisitados'),
    path('recusar_requerimento/<int:livro_id>', views.RecusarRequerimento.as_view(),name='recusar_requerimento'),
    ]