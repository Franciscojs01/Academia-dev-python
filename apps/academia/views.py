from django.shortcuts import get_object_or_404, render
from django.db import connection, models
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from .models import Aluno, Curso, Matricula
from .permissions import IsAdminOrOwner
from .serializers import AlunoSerializer, CursoSerializer, MatriculaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAdminUser]


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Matricula.objects.all()

        aluno = get_object_or_404(Aluno, user=user)
        return Matricula.objects.filter(aluno=aluno)

    def create(self, request, *args, **kwargs):
        aluno = get_object_or_404(Aluno, user=request.user)

        serializer = MatriculaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        curso = serializer.validated_data['curso']
        valor = curso.valor_inscricao

        matricula = Matricula.objects.create(
            aluno=aluno,
            curso=curso,
            valor=valor,
            status_pagamento='pendente',
        )

        return Response(
            MatriculaSerializer(matricula).data,
            status=status.HTTP_201_CREATED
        )

    @api_view(['GET'])
    def listar_matriculas_aluno(request, aluno_id):
        if request.user.is_superuser:
            qs = Matricula.objects.filter(aluno_id=aluno_id)
            return Response(MatriculaSerializer(qs, many=True).data)

        aluno = get_object_or_404(Aluno, user=request.user)

        if aluno.id != aluno_id:
            return Response({"detail": "Acesso negado."}, status=403)

        qs = Matricula.objects.filter(aluno=aluno)
        return Response(MatriculaSerializer(qs, many=True).data)


    @api_view(['POST'])
    def marcar_matricula_paga(request, pk):
        matricula = get_object_or_404(Matricula, pk=pk)
        matricula.status_pagamento = 'pago'
        matricula.save()
        return Response(MatriculaSerializer(matricula).data)


    @api_view(['GET'])
    def total_matriculas_por_curso(request):
        """
        Relatório obrigatório usando SQL bruto com JOIN + GROUP BY.
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT c.id,
                                  c.nome,
                                  COUNT(m.id) AS total_matriculas
                           FROM academia_curso c
                                    LEFT JOIN academia_matricula m ON m.curso_id = c.id
                           GROUP BY c.id, c.nome
                           ORDER BY total_matriculas DESC;
                           """)

            cols = [col[0] for col in cursor.description]
            results = [dict(zip(cols, row)) for row in cursor.fetchall()]

        return Response(results)

def dashboard(request):
    # Total de alunos
    total_alunos = Aluno.objects.count()

    # Total de cursos
    total_cursos = Curso.objects.count()

    # Total de matrículas
    total_matriculas = Matricula.objects.count()

    # Total arrecadado
    total_pago = Matricula.objects.filter(status_pagamento="pago").aggregate(
        total=models.Sum("valor")
    )["total"] or 0

    context = {
        "total_alunos": total_alunos,
        "total_cursos": total_cursos,
        "total_matriculas": total_matriculas,
        "total_pago": total_pago,
    }

    return render(request, "dashboard.html", context)

def aluno_historico(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    matriculas = Matricula.objects.filter(aluno=aluno).select_related("curso")

    total_pago = matriculas.filter(status_pagamento="pago").aggregate(
        total=models.Sum("valor")
    )["total"] or 0

    total_pendente = matriculas.filter(status_pagamento="pendente").aggregate(
        total=models.Sum("valor")
    )["total"] or 0

    context = {
        "aluno": aluno,
        "matriculas": matriculas,
        "total_pago": total_pago,
        "total_pendente": total_pendente,
    }

    return render(request, "aluno_historico.html", context)
