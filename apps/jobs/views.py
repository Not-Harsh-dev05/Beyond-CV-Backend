"""Job-role listing and recruiter creation."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiter
from apps.core.responses import success
from .models import JobRole
from .serializers import JobRoleSerializer


class JobListCreateView(generics.ListCreateAPIView):
    """Recruiters create jobs; authenticated users see available roles."""

    serializer_class = JobRoleSerializer
    permission_classes = [IsAuthenticated]
    queryset = JobRole.objects.all().order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsRecruiter()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)

    def create(self, request, *args, **kwargs):
        from rest_framework import status

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return success(serializer.data, status=status.HTTP_201_CREATED, request=request)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
