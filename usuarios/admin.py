from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Colaborador

User = get_user_model()

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "perfil", "ativo", "usuario")
    list_filter = ("perfil", "ativo")
    search_fields = ("nome", "matricula", "cpf")

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'colaborador') and request.user.colaborador.perfil == 'ADMIN':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'colaborador') and request.user.colaborador.perfil == 'ADMIN':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'colaborador'):
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        if hasattr(request.user, 'colaborador') and request.user.colaborador.perfil == 'ADMIN':
            return ()
        return ("nome", "matricula", "cpf", "perfil", "ativo", "usuario")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Perfis que precisam de usuário
        perfis_com_login = ['TECNICO_SST', 'ALMOXARIFE']
        if obj.perfil in perfis_com_login and not obj.usuario:
            username = obj.nome.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                try:
                    user = User.objects.create_user(
                        username=username,
                        password='senha',  # trocar depois
                        is_staff=True
                    )
                    obj.usuario = user
                    obj.save()
                    print(f"Usuário '{username}' criado com sucesso!")
                except IntegrityError:
                    print(f"Falha: O usuário '{username}' já existe.")