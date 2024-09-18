from django.db import models
import uuid
from django.contrib.auth.models import User

class TypeEnergy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(
        verbose_name="Tipo", max_length=100, unique=True, null=False, blank=False, help_text="Tipo de energia")
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tipo
    

class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usando o User padrão
    energiaAnterior = models.ForeignKey(TypeEnergy, on_delete=models.CASCADE, related_name='progress_energia_anterior')
    energiaAtual = models.ForeignKey(TypeEnergy, on_delete=models.CASCADE, related_name='progress_energia_atual')
    custoAnterior = models.DecimalField(
        verbose_name="CustoAnterior", max_digits=10, decimal_places=2, null=False, blank=False, help_text="Preço anterior")
    custoAtual = models.DecimalField(
        verbose_name="CustoAtual", max_digits=10, decimal_places=2, null=False, blank=False, help_text="Preço atual")
    duracao = models.DecimalField(
        verbose_name="Duracao", max_digits=10, decimal_places=2, null=False, blank=False, help_text="Jornada")
    dt = models.DateTimeField(auto_now_add=True)
