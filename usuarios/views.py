from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

from .models import Colaborador
from .forms import ColaboradorForm


class UsuarioLoginView(LoginView):
    template_name = "usuarios/login.html"
    redirect_authenticated_user = True


class UsuarioLogoutView(LogoutView):
    next_page = reverse_lazy("usuarios:login")


@login_required
def dashboard_view(request):
    """
    Exibe o dashboard principal.
    Apenas usuários autenticados podem acessar.
    """
    return render(request, "dashboard/dashboard.html")


@login_required
def perfil_editar_view(request):
    """
    Exibe a página de edição de perfil do usuário.
    """
    return render(request, "usuarios/perfil_editar.html")


class ColaboradorCreateView(UserPassesTestMixin, CreateView):
    """
    Admin e Almoxarife podem criar colaboradores.
    Se for Almoxarife, o perfil do colaborador
    é automaticamente 'COLABORADOR'.
    """
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'usuarios/colaborador_form.html'
    success_url = reverse_lazy("usuarios:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa o request para o form para travar o campo perfil
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        perfil = getattr(getattr(self.request.user, 'colaborador', None), 'perfil', None)
        return self.request.user.is_superuser or perfil in ['ADMIN', 'ALMOXARIFE']


class ColaboradorListView(ListView):
    """
    Lista de colaboradores – visível para todos usuários autenticados.
    """
    model = Colaborador
    template_name = "usuarios/list.html"
    context_object_name = 'colaboradores'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) | Q(matricula__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class ColaboradorUpdateView(UserPassesTestMixin, UpdateView):
    """
    Apenas Admin ou superuser podem editar colaboradores.
    """
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'usuarios/colaborador_form.html'
    success_url = reverse_lazy("usuarios:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, 'colaborador') and
            self.request.user.colaborador.perfil == 'ADMIN'
        )


class ColaboradorDeleteView(UserPassesTestMixin, DeleteView):
    """
    Apenas Admin ou superuser podem excluir colaboradores.
    """
    model = Colaborador
    template_name = "usuarios/colaborador_confirm_delete.html"
    success_url = reverse_lazy("usuarios:list")

    def test_func(self):
        return self.request.user.is_superuser or (
            hasattr(self.request.user, 'colaborador') and
            self.request.user.colaborador.perfil == 'ADMIN'
        )
