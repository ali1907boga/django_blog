from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and request.user.is_superuser or
            request.user.is_authenticated and obj.author == request.user

         )



class IsSuperUserOrStaffReadOnly(BasePermission):

    def has_permission(self, request, view):
        #because we use SAFEMETHODS just readonly
        if request.method in SAFE_METHODS and request.user.is_staff and request.user.is_authenticated:
            return True
        # full permissions because we not use SAFE_METHODS
        return bool(
           request.user.is_superuser and request.user.is_authenticated
        )

