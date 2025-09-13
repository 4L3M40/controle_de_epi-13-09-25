from django.shortcuts import render
from django.db.models import Q
from emprestimos.models import EmprestimoItem

def relatorio_colaborador(request):
    q = request.GET.get('q','').strip()
    itens = EmprestimoItem.objects.select_related('emprestimo__colaborador','epi','emprestimo')
    if q:
        itens = itens.filter(Q(emprestimo__colaborador__nome__icontains=q))
    context = {'q': q, 'itens': itens}
    return render(request, 'relatorios/relatorio_colaborador.html', context)
