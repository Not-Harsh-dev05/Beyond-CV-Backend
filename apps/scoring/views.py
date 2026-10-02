"""Restricted pedigree model management API."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.accounts.permissions import IsAdmin
from apps.core.responses import success, failure
from apps.scoring.pedigree import train_model


class PedigreeTrainView(APIView):
    """Admin-only model retraining from a server-local CSV path."""

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        path = request.data.get("data_path")
        if not path:
            return failure(
                "invalid_input", "data_path is required.", status=400, request=request
            )
        try:
            output = train_model(path)
        except (OSError, ValueError) as exc:
            return failure("training_failed", str(exc), status=400, request=request)
        return success({"trained": True, "artifact": output}, request=request)
