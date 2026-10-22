from django.db import models
from petis.models import Atendimento
from django.contrib.auth.models import User

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada (Receita)'),
        ('SAIDA', 'Saída (Despesa)'),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ('PIX', 'Pix'),
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
    ]

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='ENTRADA')
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, default='PIX')
    data = models.DateField()
    atendimento = models.ForeignKey(Atendimento, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacoes')
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendedor")

    def __str__(self):
        return f"{self.tipo} - {self.descricao} - R$ {self.valor}"
    



