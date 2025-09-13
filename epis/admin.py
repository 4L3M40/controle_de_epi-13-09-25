from django.contrib import admin
from .models import Epi

@admin.register(Epi)
class EpiAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'status', 'estoque', 'ativo')