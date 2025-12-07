from django.urls import path, include
from .views import (
    AlunoViewSet,
    CursoViewSet,
    MatriculaViewSet,
    dashboard,
    aluno_historico
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'matriculas', MatriculaViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # API
    path('matriculas/aluno/<int:aluno_id>/', MatriculaViewSet.listar_matriculas_aluno),
    path('matriculas/<int:pk>/marcar-paga/', MatriculaViewSet.marcar_matricula_paga),
    path('relatorios/total-matriculas/', MatriculaViewSet.total_matriculas_por_curso),

    # HTML Pages
    path('dashboard/', dashboard, name="dashboard"),
    path('alunos/<int:aluno_id>/historico/', aluno_historico, name="aluno_historico"),
]
