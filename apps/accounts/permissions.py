"""Role-based view and object permissions."""

from rest_framework.permissions import BasePermission


class IsRole(BasePermission):
    """Allow only explicitly configured roles."""

    roles = ()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in self.roles
        )

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "user", None)
        return request.user.role == "ADMIN" or owner == request.user


class IsCandidate(IsRole):
    """Candidate-only access."""

    roles = ("CANDIDATE", "ADMIN")


class IsRecruiter(IsRole):
    """Recruiter or administrator access."""

    roles = ("RECRUITER", "ADMIN")


class IsAdmin(IsRole):
    """Administrator-only access."""

    roles = ("ADMIN",)


class IsCandidateOwner(IsRole):
    """Candidate can access only owned records; admins can support requests."""

    roles = ("CANDIDATE", "ADMIN")

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True
        return getattr(obj, "user_id", None) == request.user.id
