from datetime import timezone
from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_ingresso = models.DateField(default=timezone)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Curso(models.Model):
    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'))

    nome = models.CharField(max_length=200)
    carga_horaria = models.PositiveIntegerField()
    valor_inscricao = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return self.nome


class Matricula(models.Model):
    STATUS_PAGAMENTO = (('pago', 'Pago'), ('pendente', 'Pendente'))
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=timezone)
    status_pagamento = models.CharField(max_length=10, choices=STATUS_PAGAMENTO, default='pendente')


    class Meta:
        unique_together = ('aluno', 'curso')

    def __str__(self):
        return f"{self.aluno} -> {self.curso} [{self.status_pagamento}]"


