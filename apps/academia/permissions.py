from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    """
    Admin pode tudo.
    Aluno só pode acessar objetos dele.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Matricula
        if hasattr(obj, "aluno"):
            return obj.aluno.user == request.user

        # Aluno
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
