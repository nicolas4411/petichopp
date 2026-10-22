from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Importante!


class Pet(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50)
    idade = models.PositiveIntegerField()
    dono = models.CharField(max_length=100)
    telefone_dono = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)  # Soft Delete

    def __str__(self):
        return f"{self.nome} ({self.especie}) - Tutor: {self.dono} (Telefone: {self.telefone_dono})"


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco_padrao = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor do Serviço"
    )

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_padrao}"


class Atendimento(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='atendimentos')
    data = models.DateField(default=timezone.now)
    servicos_descricao = models.TextField(help_text="Lista dos serviços executados")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendedor/Atendente")

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} - {self.pet.nome} (Tutor: {self.pet.dono}) - R$ {self.valor_total}"
    


