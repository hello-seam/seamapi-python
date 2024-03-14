from seamapi.types import AbstractAcsCredentials, AbstractSeam as Seam
from typing import Optional, Any, List, Dict, Union


class AcsCredentials(AbstractAcsCredentials):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def assign(self, acs_user_id: str, acs_credential_id: str) -> None:
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/assign", json=json_payload)

        return None

    def create(
        self,
        acs_user_id: str,
        access_method: str,
        code: Optional[str] = None,
        is_multi_phone_sync_credential: Optional[bool] = None,
        external_type: Optional[str] = None,
        visionline_metadata: Optional[Dict[str, Any]] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
    ) -> None:
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if access_method is not None:
            json_payload["access_method"] = access_method
        if code is not None:
            json_payload["code"] = code
        if is_multi_phone_sync_credential is not None:
            json_payload[
                "is_multi_phone_sync_credential"
            ] = is_multi_phone_sync_credential
        if external_type is not None:
            json_payload["external_type"] = external_type
        if visionline_metadata is not None:
            json_payload["visionline_metadata"] = visionline_metadata
        if starts_at is not None:
            json_payload["starts_at"] = starts_at
        if ends_at is not None:
            json_payload["ends_at"] = ends_at

        self.seam.make_request("POST", "/acs/credentials/create", json=json_payload)

        return None

    def delete(self, acs_credential_id: str) -> None:
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/delete", json=json_payload)

        return None

    def get(self, acs_credential_id: str) -> None:
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/get", json=json_payload)

        return None

    def list(self, is_multi_phone_sync_credential: Optional[bool] = None) -> None:
        json_payload = {}

        if is_multi_phone_sync_credential is not None:
            json_payload[
                "is_multi_phone_sync_credential"
            ] = is_multi_phone_sync_credential

        self.seam.make_request("POST", "/acs/credentials/list", json=json_payload)

        return None

    def unassign(self, acs_user_id: str, acs_credential_id: str) -> None:
        json_payload = {}

        if acs_user_id is not None:
            json_payload["acs_user_id"] = acs_user_id
        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id

        self.seam.make_request("POST", "/acs/credentials/unassign", json=json_payload)

        return None

    def update(self, acs_credential_id: str, code: str) -> None:
        json_payload = {}

        if acs_credential_id is not None:
            json_payload["acs_credential_id"] = acs_credential_id
        if code is not None:
            json_payload["code"] = code

        self.seam.make_request("POST", "/acs/credentials/update", json=json_payload)

        return None
