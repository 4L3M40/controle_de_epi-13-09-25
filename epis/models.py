from django.db import models

class Epi(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    ca_numero = models.CharField(max_length=30, blank=True, null=True)
    ca_validade = models.DateField(blank=True, null=True)
    tamanho = models.CharField(max_length=20, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    STATUS_CHOICES = [
        ('FORNECIDO', 'Fornecido'),
        ('EMPRESTADO', 'Emprestado'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FORNECIDO')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.codigo})"
