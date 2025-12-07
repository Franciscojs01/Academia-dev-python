from rest_framework import serializers
from .models import Aluno, Curso, Matricula

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'email', 'cpf', 'data_ingresso']
        read_only_fields = ['id', 'data_ingresso']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    aluno = AlunoSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)

    curso_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Curso.objects.all(), source='curso'
    )

    class Meta:
        model = Matricula
        fields = ['id', 'aluno', 'curso', 'curso_id','valor', 'status_pagamento', 'data']
        read_only_fields = ['id', 'data', 'aluno', 'valor']