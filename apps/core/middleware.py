"""Request correlation and load-balancer instance headers."""

import socket
import uuid


class RequestMetadataMiddleware:
    """Attach a request ID and serving hostname to every response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[
            :128
        ]
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id
        response["X-Served-By"] = socket.gethostname()
        return response
