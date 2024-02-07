from seamapi.types import AbstractHealth, AbstractSeam as Seam
from typing import Optional, Any
from seamapi.health_service import HealthService


class Health(AbstractHealth):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam
        self._service = HealthService(seam=seam)

    @property
    def service(self) -> HealthService:
        return self._service

    def get_health(
        self,
    ):
        json_payload = {}

        self.seam.make_request("POST", "/health/get_health", json=json_payload)

        return None

    def get_service_health(self, service: Any):
        json_payload = {}

        if service is not None:
            json_payload["service"] = service

        self.seam.make_request("POST", "/health/get_service_health", json=json_payload)

        return None
