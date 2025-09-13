from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages import success, error
from .models import Epi
from .forms import EpiForm

class EpiListView(UserPassesTestMixin, ListView):
    model = Epi
    template_name = "epis/epi_list.html"

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'TECNICO_SST', 'ALMOXARIFE']

class EpiCreateView(UserPassesTestMixin, CreateView):
    model = Epi
    form_class = EpiForm
    template_name = "epis/epi_form.html"
    success_url = reverse_lazy("epis:list")

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return (self.request.user.is_superuser or perfil in ['ADMIN','TECNICO_SST','ALMOXARIFE','TECNICO','TECNICO_SST'])

    def form_valid(self, form):
        success(self.request, "EPI criado com sucesso!")
        return super().form_valid(form)

class EpiUpdateView(UserPassesTestMixin, UpdateView):
    model = Epi
    form_class = EpiForm
    template_name = "epis/epi_form.html"
    success_url = reverse_lazy("epis:list")

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'TECNICO_SST', 'ALMOXARIFE']

    def form_valid(self, form):
        success(self.request, "EPI atualizado com sucesso!")
        return super().form_valid(form)

class EpiDeleteView(UserPassesTestMixin, DeleteView):
    model = Epi
    template_name = "epis/epi_confirm_delete.html"
    success_url = reverse_lazy("epis:list")

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'TECNICO_SST', 'ALMOXARIFE']

    def form_valid(self, form):
        success(self.request, "EPI excluído com sucesso!")
        return super().form_valid(form)