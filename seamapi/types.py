# TODO this file should eventually be generated by looking at openapi.json

import abc
from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from seamapi.utils.deep_attr_dict import DeepAttrDict

AccessCodeId = str
ActionAttemptId = str
DeviceId = str
EventId = str
AcceptedProvider = str  # e.g. august or noiseaware
ConnectWebviewId = str
ConnectedAccountId = str
Email = str
DeviceType = str  # e.g. august_lock
WorkspaceId = str


class SeamAPIException(Exception):
    def __init__(
        self,
        status_code: int,
        request_id: str,
        metadata: Optional[Dict[str, any]],
    ):
        self.status_code = status_code
        self.request_id = request_id
        self.metadata = metadata

        super().__init__(
            f"SeamAPIException: status={status_code}, request_id={request_id}, metadata={metadata}"
        )


class ActionAttemptFailedException(Exception):
    def __init__(
        self,
        action_attempt_id: Optional[str] = None,
        action_type: Optional[str] = None,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        self.action_attempt_id = action_attempt_id
        self.action_type = action_type
        self.error_type = error_type
        self.error_message = error_message
        super().__init__(
            f'Action Attempt for "{action_type}" Failed. {error_type}: {error_message} (action_attempt_id={action_attempt_id})'
        )


class WaitForAccessCodeFailedException(Exception):
    def __init__(
        self, message: str, access_code_id: str, errors: Optional[list] = []
    ):
        self.access_code_id = access_code_id
        self.errors = errors
        super().__init__(f"Failed while waiting for access code. ${message}")


@dataclass
class Device:
    device_id: DeviceId
    device_type: str
    location: Optional[Dict[str, Any]]
    properties: Any
    capabilities_supported: List[str]
    errors: List[Dict[str, Any]]

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        return Device(
            device_id=d["device_id"],
            device_type=d["device_type"],
            location=d.get("location", None),
            properties=DeepAttrDict(d["properties"]),
            capabilities_supported=d["capabilities_supported"],
            errors=d["errors"],
        )


@dataclass_json
@dataclass
class UnmanagedDevice:
    device_id: DeviceId
    device_type: str
    errors: List[Dict[str, Any]]


@dataclass
class Event:
    event_id: str
    event_class: Union[str, None]
    event_type: Union[str, None]
    device_id: Optional[str]
    created_at: Union[str, None]


@dataclass_json
@dataclass
class ActionAttemptError:
    type: str
    message: str


@dataclass_json
@dataclass
class ActionAttempt:
    action_attempt_id: str
    action_type: str
    status: str
    result: Optional[Any]
    error: Optional[ActionAttemptError]


@dataclass_json
@dataclass
class Workspace:
    workspace_id: str
    name: str
    is_sandbox: bool


@dataclass_json
@dataclass
class ConnectWebview:
    workspace_id: str
    connect_webview_id: str
    status: str
    url: str
    login_successful: bool
    device_selection_mode: str
    any_provider_allowed: bool
    any_device_allowed: bool
    created_at: str
    custom_metadata: Dict[str, Union[str, int, bool, None]]
    connected_account_id: Optional[str] = None
    authorized_at: Optional[str] = None
    custom_redirect_url: Optional[str] = None
    custom_redirect_failure_url: Optional[str] = None
    accepted_providers: Optional[List[AcceptedProvider]] = None
    accepted_devices: Optional[List[str]] = None
    selected_provider: Optional[str] = None


@dataclass_json
@dataclass
class ConnectedAccount:
    connected_account_id: str
    created_at: str
    user_identifier: str
    account_type: str
    errors: List[str]
    custom_metadata: Dict[str, Union[str, int, bool, None]]


@dataclass_json
@dataclass
class AccessCode:
    access_code_id: str
    type: str
    code: str
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    name: Optional[str] = ""
    status: Optional[str] = None
    common_code_key: Optional[str] = None


@dataclass
class NoiseThreshold:
    noise_threshold_id: str
    device_id: str
    name: str
    noise_threshold_decibels: float

    starts_daily_at: Optional[str]
    ends_daily_at: Optional[str]

    noise_threshold_nrs: Optional[float]

    @staticmethod
    def from_dict(nt: Dict[str, Any]):
        return NoiseThreshold(
            noise_threshold_id=nt["noise_threshold_id"],
            device_id=nt["device_id"],
            name=nt["name"],
            noise_threshold_decibels=nt["noise_threshold_decibels"],
            starts_daily_at=nt["starts_daily_at"],
            ends_daily_at=nt["ends_daily_at"],
            noise_threshold_nrs=nt.get("noise_threshold_nrs", None),
        )


class AbstractActionAttempts(abc.ABC):
    @abc.abstractmethod
    def get(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        raise NotImplementedError

    @abc.abstractmethod
    def poll_until_ready(
        self,
        action_attempt: Union[ActionAttemptId, ActionAttempt],
        should_raise: bool = True,
    ) -> ActionAttempt:
        raise NotImplementedError


class AbstractLocks(abc.ABC):
    @abc.abstractmethod
    def list(self, connected_account: Optional[str] = None) -> List[Device]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, device: Union[DeviceId, Device]) -> Device:
        raise NotImplementedError

    @abc.abstractmethod
    def lock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        raise NotImplementedError

    @abc.abstractmethod
    def unlock_door(self, device: Union[DeviceId, Device]) -> ActionAttempt:
        raise NotImplementedError


class AbstractAccessCodes(abc.ABC):
    @abc.abstractmethod
    def list(self, device: Union[DeviceId, Device]) -> List[AccessCode]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self,
        access_code: Union[AccessCodeId, AccessCode],
    ) -> AccessCode:
        raise NotImplementedError

    @abc.abstractmethod
    def create_multiple(
        self,
        devices: Union[List[DeviceId], List[Device]],
        name: Optional[str] = None,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        common_code_key: Optional[str] = None,
    ) -> List[AccessCode]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(
        self,
        device: Union[DeviceId, Device],
        name: Optional[str] = None,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        common_code_key: Optional[str] = None,
    ) -> AccessCode:
        raise NotImplementedError

    @abc.abstractmethod
    def update(
        self,
        access_code: Union[AccessCodeId, AccessCode],
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
        code: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        status: Optional[str] = None,
    ) -> AccessCode:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(
        self,
        access_code: Union[AccessCodeId, AccessCode],
    ) -> ActionAttempt:
        raise NotImplementedError


class AbstractNoiseThresholds(abc.ABC):
    @abc.abstractmethod
    def create(
        self,
        device_id: str,
        starts_daily_at: str,
        ends_daily_at: str,
        name: Optional[str],
        noise_threshold_decibels: Optional[float] = None,
        noise_threshold_nrs: Optional[float] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> Union[ActionAttempt, NoiseThreshold]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(
        self,
        device_id: str,
        noise_threshold_id: str,
        name: Optional[str] = None,
        starts_daily_at: Optional[str] = None,
        ends_daily_at: Optional[str] = None,
        noise_threshold_decibels: Optional[str] = None,
        noise_threshold_nrs: Optional[str] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> Union[ActionAttempt, NoiseThreshold]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(
        self,
        device_id: str,
    ) -> List[NoiseThreshold]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(
        self,
        noise_threshold_id: str,
        device_id: str,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        raise NotImplementedError


class AbstractNoiseSensors(abc.ABC):
    @property
    @abc.abstractmethod
    def noise_thresholds(self) -> AbstractNoiseThresholds:
        raise NotImplementedError

    @abc.abstractmethod
    def list_noise_levels(
        self, starting_after=None, ending_before=None
    ) -> None:
        raise NotImplementedError


class AbstractDevices(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[Device]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> Device:
        raise NotImplementedError


class AbstractUnmanagedDevices(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[UnmanagedDevice]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self) -> bool:
        raise NotImplementedError


class AbstractEvents(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[Event]:
        raise NotImplementedError


class AbstractWorkspaces(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[Workspace]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, workspace_id: Optional[str] = None) -> Workspace:
        raise NotImplementedError

    @abc.abstractmethod
    def reset_sandbox(self) -> None:
        raise NotImplementedError


class AbstractConnectWebviews(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[ConnectWebview]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, connect_webview_id: str) -> ConnectWebview:
        raise NotImplementedError

    @abc.abstractmethod
    def create(
        self, accepted_providers: Optional[List[AcceptedProvider]] = None
    ) -> ConnectWebview:
        raise NotImplementedError


class AbstractConnectedAccounts(abc.ABC):
    @abc.abstractmethod
    def list(self) -> List[ConnectedAccount]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self, connected_account: Union[ConnectedAccountId, ConnectedAccount]
    ) -> ConnectedAccount:
        raise NotImplementedError


@dataclass
class AbstractRoutes(abc.ABC):
    workspaces: AbstractWorkspaces
    connect_webviews: AbstractConnectWebviews
    locks: AbstractLocks
    devices: AbstractDevices
    access_codes: AbstractAccessCodes
    action_attempts: AbstractActionAttempts
    noise_sensors: AbstractNoiseSensors

    @abc.abstractmethod
    def make_request(self, method: str, path: str, **kwargs) -> Any:
        raise NotImplementedError


@dataclass
class AbstractSeam(AbstractRoutes):
    api_key: str
    api_url: str

    @abc.abstractmethod
    def __init__(self, api_key: Optional[str] = None):
        raise NotImplementedError


@dataclass_json
@dataclass
class ResetSandBoxResponse:
    message: str
    ok: bool
