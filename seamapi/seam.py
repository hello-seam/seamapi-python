import os
from typing import Optional
from .workspaces import Workspaces
from .types import AbstractSeam


class Seam(AbstractSeam):
    api_key: str
    api_url = "https://connect.getseam.com"

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ.get("SEAM_API_KEY", None)
        if api_key is None:
            raise Exception(
                "SEAM_API_KEY not found in environment, and api_key not provided"
            )
        self.api_key = api_key
        self.api_url = os.environ.get("api_url", self.api_url)
        self.workspaces = Workspaces(seam=self)
