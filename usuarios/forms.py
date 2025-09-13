from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Colaborador
        fields = ['nome', 'cpf', 'matricula', 'perfil', 'ativo']

    def __init__(self, *args, **kwargs):
        # Recebe o request das views para saber quem está criando/editando
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Se for Almoxarife logado, trava o campo 'perfil' como COLABORADOR
        if self.request and hasattr(self.request.user, 'colaborador'):
            if self.request.user.colaborador.perfil == 'ALMOXARIFE':
                self.fields['perfil'].initial = 'COLABORADOR'
                self.fields['perfil'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        perfil   = cleaned_data.get('perfil')

        # Se for Almoxarife, força o perfil mesmo que tentem mudar via POST
        if self.request and hasattr(self.request.user, 'colaborador'):
            if self.request.user.colaborador.perfil == 'ALMOXARIFE':
                cleaned_data['perfil'] = 'COLABORADOR'
                perfil = 'COLABORADOR'

        perfis_com_login = ['TECNICO_SST', 'ALMOXARIFE', 'ADMIN']

        if perfil in perfis_com_login:
            if not username:
                self.add_error('username', 'Este campo é obrigatório para o perfil selecionado.')
            if not password:
                self.add_error('password', 'Este campo é obrigatório para o perfil selecionado.')
        elif perfil == 'COLABORADOR':
            if username:
                self.add_error('username', 'Para Colaborador, não preencha este campo. Deixe vazio.')
            if password:
                self.add_error('password', 'Para Colaborador, não preencha este campo. Deixe vazio.')

        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Nome de usuário já existe.")

        return cleaned_data

    def save(self, commit=True):
        colaborador = super().save(commit=False)
        perfil = self.cleaned_data['perfil']

        # Cria usuário vinculado apenas para perfis que exigem login
        if perfil in ['TECNICO_SST', 'ALMOXARIFE', 'ADMIN']:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            if username and password:
                user = User.objects.create_user(username=username, password=password)
                colaborador.usuario = user

        if commit:
            colaborador.save()
        return colaborador
