from django.db import models
from django.utils import timezone
from usuarios.models import Colaborador
from epis.models import Epi
from django.contrib.auth.models import User

class Emprestimo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    previsao_devolucao = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('FECHADO', 'Fechado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ABERTO')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"Empréstimo {self.id} para {self.colaborador.nome}"

    def clean(self):
        # Opcional: garantir que a previsão seja futura
        if self.previsao_devolucao and self.previsao_devolucao <= timezone.now():
            from django.core.exceptions import ValidationError
            raise ValidationError({"previsao_devolucao": "A data prevista para devolução deve ser futura."})


class EmprestimoItem(models.Model):
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('EM_USO', 'Em Uso'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]
    STATUS_CHOICES = [
        ('EMPRESTADO', 'Emprestado'),
        ('FORNECIDO', 'Fornecido'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]

    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE, related_name='itens')
    epi = models.ForeignKey(Epi, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    entregue_em = models.DateTimeField(auto_now_add=True)
    devolvido_em = models.DateTimeField(blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    # Novo campo conforme especificação do controle de EPI
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EMPRESTADO')

    def _str_(self):
        return f"Item {self.epi.nome} ({self.quantidade}) — {self.status} — Empréstimo {self.emprestimo.id}"