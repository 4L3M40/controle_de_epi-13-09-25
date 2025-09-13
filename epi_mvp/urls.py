from django.contrib import admin
from django.urls import path, include
from relatorios.views import relatorio_colaborador
from django.contrib.auth.decorators import login_required
from usuarios.views import dashboard_view  # Atualizado para usuarios

urlpatterns = [
    path('relatorios/colaborador/', relatorio_colaborador, name='relatorio_colaborador'),
    path("admin/", admin.site.urls),
    
    # Rota inicial redireciona para dashboard
    path("", login_required(dashboard_view), name="dashboard"),
    
    path("dashboard/", login_required(dashboard_view), name="dashboard"),
    
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),
    
    path("epis/", include("epis.urls", namespace="epis")),
    
    path("emprestimos/", include("emprestimos.urls", namespace="emprestimos")),
]