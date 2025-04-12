from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """PERMISSION PERSONNALISÉ POUR PERMETTRE A L'AUTEUR D'UN ARTICLE D'AVOIR LES DROITS UNIQUEMENT SUR SES ARTICLES , ET LE SUPERUSER A ACCES A TOUT"""
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.auteur==request.user or request.user.is_superuser
    
class Isadmin(permissions.BasePermission):
    """PERMISSSION POUR L'ADMIN """
    
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.is_staff #verifie que l'utilisateur est admin 
