from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin  # Para mensagens
from .models import Emprestimo, EmprestimoItem
from .forms import EmprestimoForm, EmprestimoItemFormSet
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages

class ReadonlyContextMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        # Permissões: ALMOXARIFE e ADMIN podem criar/editar; TECNICO_SST só visualiza
        readonly = not (self.request.user.is_superuser or perfil in ['ADMIN', 'ALMOXARIFE'])
        ctx['readonly'] = readonly
        return ctx


class EmprestimoListView(UserPassesTestMixin, ListView):
    model = Emprestimo
    template_name = "emprestimos/emprestimo_list.html"
    context_object_name = 'emprestimos'
    paginate_by = 10

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'TECNICO_SST', 'ALMOXARIFE']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(colaborador__nome__icontains=q) | Q(status__icontains=q))
        return queryset

class EmprestimoCreateView(ReadonlyContextMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "emprestimos/emprestimo_form.html"
    success_url = reverse_lazy("emprestimos:list")
    success_message = "Empréstimo registrado com sucesso!"

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'ALMOXARIFE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = EmprestimoItemFormSet(self.request.POST)
        else:
            context['item_formset'] = EmprestimoItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.usuario_registro = self.request.user
            self.object.save()
            item_formset.instance = self.object
            item_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class EmprestimoUpdateView(ReadonlyContextMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "emprestimos/emprestimo_form.html"
    success_url = reverse_lazy("emprestimos:list")  # Corrigido: adicionado )
    success_message = "Empréstimo atualizado com sucesso!"

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'ALMOXARIFE']

class EmprestimoDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Emprestimo
    template_name = "emprestimos/emprestimo_confirm_delete.html"
    success_url = reverse_lazy("emprestimos:list")  # Corrigido: adicionado )
    success_message = "Empréstimo excluído com sucesso!"

    def test_func(self):
        perfil = self.request.user.colaborador.perfil if hasattr(self.request.user, 'colaborador') else None
        return self.request.user.is_superuser or perfil in ['ADMIN', 'ALMOXARIFE']