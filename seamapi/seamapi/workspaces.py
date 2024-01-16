from seamapi.types import AbstractWorkspaces, AbstractSeam as Seam, Workspace
from typing import Optional, Any


class Workspaces(AbstractWorkspaces):
    seam: Seam

    def __init__(self, seam: Seam):
        self.seam = seam

    def create(
        self,
        name: Optional[Any] = None,
        connect_partner_name: Optional[Any] = None,
        is_sandbox: Optional[Any] = None,
        webview_primary_button_color: Optional[Any] = None,
        webview_logo_shape: Optional[Any] = None,
    ):
        json_payload = {}
        if name is not None:
            json_payload["name"] = name
        if connect_partner_name is not None:
            json_payload["connect_partner_name"] = connect_partner_name
        if is_sandbox is not None:
            json_payload["is_sandbox"] = is_sandbox
        if webview_primary_button_color is not None:
            json_payload["webview_primary_button_color"] = webview_primary_button_color
        if webview_logo_shape is not None:
            json_payload["webview_logo_shape"] = webview_logo_shape
        res = self.seam.make_request("POST", "/workspaces/create", json=json_payload)
        return None.from_dict(res[""])

    def get(
        self,
    ):
        json_payload = {}
        res = self.seam.make_request("POST", "/workspaces/get", json=json_payload)
        return Workspace.from_dict(res["workspace"])

    def list(
        self,
    ):
        json_payload = {}
        res = self.seam.make_request("POST", "/workspaces/list", json=json_payload)
        return [Workspace.from_dict(item) for item in res["workspaces"]]

    def reset_sandbox(
        self,
    ):
        json_payload = {}
        res = self.seam.make_request(
            "POST", "/workspaces/reset_sandbox", json=json_payload
        )
        return None.from_dict(res["message"])
