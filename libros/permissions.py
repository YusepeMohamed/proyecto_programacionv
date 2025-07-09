from rest_framework import permissions

class EsCreadorODenegado(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Solo el creador puede editar o eliminar
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creador == request.user


class EsAutorPuntuacionODenegado(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario == request.user