"""Role-aware DRF request throttling."""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RoleRateThrottle(UserRateThrottle, AnonRateThrottle):
    """Apply a per-role limit using configured role rates."""

    scope = "candidate"

    def allow_request(self, request, view):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            self.scope = "anon"
            throttle = AnonRateThrottle
        else:
            self.scope = "admin" if user.role == "ADMIN" else user.role.lower()
            throttle = UserRateThrottle
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)
        return throttle.allow_request(self, request, view)
