from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# View do dashboard
@login_required
def dashboard_view(request):
    """
    Exibe o dashboard principal.
    Apenas usuários autenticados podem acessar.
    """
    return render(request, "dashboard/dashboard.html")  # Ajuste o caminho do template se necessário
