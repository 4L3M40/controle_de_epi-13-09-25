from django.contrib import admin
from .models import Emprestimo, EmprestimoItem

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'colaborador', 'status', 'data_emprestimo')

@admin.register(EmprestimoItem)
class EmprestimoItemAdmin(admin.ModelAdmin):
    list_display = ('emprestimo', 'epi', 'quantidade', 'devolvido_em')