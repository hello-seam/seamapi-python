from dataclasses import asdict
from seamapi.types import (
    NoiseThreshold,
    AbstractNoiseThresholds,
    AbstractSeam as Seam,
    ActionAttempt,
    ActionAttemptError,
)
from typing import List, Optional
import requests
import json

from seamapi.utils.report_error import report_error


class NoiseThresholds(AbstractNoiseThresholds):
    """
    A class to interact with noise thresholds through the Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(device_id)
        Gets a list of noise thresholds of a noise-monitoring device
    create(device_id, starts_daily_at, ends_daily_at, sync=None, noise_threshold_decibels=None, noise_threshold_nrs=None)
        Creates a noise threshold on a noise-monitoring device
    delete(noise_threshold_id, device_id, sync=None)
        Deletes a noise threshold on a noise-monitoring device
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Intial seam class
        """
        self.seam = seam

    @report_error
    def list(
        self,
        device_id: str,
    ) -> List[NoiseThreshold]:
        """Gets a list of noise thresholds.

        Parameters
        ----------
        device_id : str
            Device ID of a device to list noise thresholds of

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of noise thresholds.
        """
        res = self.seam.make_request(
            "GET",
            "/noise_sensors/noise_thresholds/list",
            params={"device_id": device_id},
        )

        noise_thresholds = res["noise_thresholds"]

        return [NoiseThreshold.from_dict(nt) for nt in noise_thresholds]

    @report_error
    def create(
        self,
        device_id: str,
        starts_daily_at: str,
        ends_daily_at: str,
        name: Optional[str] = None,
        noise_threshold_decibels: Optional[float] = None,
        noise_threshold_nrs: Optional[float] = None,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt | NoiseThreshold:
        """Creates a noise threshold.

        Parameters
        ----------
        device_id: str
            Device ID of a device to list noise thresholds of
        starts_daily_at: str,
            Time when noise threshold becomes active daily
        ends_daily_at: str,
            Time when noise threshold becomes inactive daily
        name: Optional[str]
            Noise threshold name
        wait_for_action_attempt: Optional[bool]
            Should wait for action attempt to resolve
        noise_threshold_decibels: Optional[float],
            The noise level in decibels
        noise_threshold_nrs: Optional[float],
            Noise Level in Noiseaware Noise Risk Score (NRS)
        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """
        params = {
            "device_id": device_id,
            "starts_daily_at": starts_daily_at,
            "ends_daily_at": ends_daily_at,
        }

        arguments = {
            "noise_threshold_decibels": noise_threshold_decibels,
            "noise_threshold_nrs": noise_threshold_nrs,
            "name": name,
        }

        for name in arguments:
            if arguments[name]:
                params.update({name: arguments[name]})

        res = self.seam.make_request(
            "POST",
            "/noise_sensors/noise_thresholds/create",
            json=params,
        )

        json_aa = res["action_attempt"]
        aa_error = None
        if "error" in json_aa and json_aa["error"] is not None:
            aa_error = ActionAttemptError(
                type=json_aa["error"]["type"],
                message=json_aa["error"]["message"],
            )

        if not wait_for_action_attempt or aa_error:
            return ActionAttempt(
                action_attempt_id=json_aa["action_attempt_id"],
                status=json_aa["status"],
                action_type=json_aa["action_type"],
                result=json_aa["result"],
                error=aa_error,
            )

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            json_aa["action_attempt_id"]
        )

        action_attempt_result = getattr(updated_action_attempt, "result", None)
        noise_threshold = action_attempt_result.get("noise_threshold", None)
        if not action_attempt_result or not noise_threshold:
            raise Exception(
                "Failed to create noise_threshold: no noise_threshold returned: "
                + json.dumps(asdict(updated_action_attempt))
            )

        return NoiseThreshold.from_dict(noise_threshold)

    @report_error
    def update(self, noise_threshold_id):
        raise NotImplementedError()

    @report_error
    def delete(
        self,
        noise_threshold_id: str,
        device_id: str,
        wait_for_action_attempt: Optional[bool] = True,
    ) -> ActionAttempt:
        """Deletes a noise threshold.

        Parameters
        ----------
        noise_threshold_id : str
            Id of a noise threshold to delete
        device_id : str
            Device ID of a device to delete noise threshold of
        wait_for_action_attempt: Optional[bool]
            Should wait for delete action attempt to resolve

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            ActionAttempt
        """
        res = self.seam.make_request(
            "DELETE",
            "/noise_sensors/noise_thresholds/delete",
            json={
                "noise_threshold_id": noise_threshold_id,
                "device_id": device_id,
            },
        )

        json_aa = res["action_attempt"]
        aa_error = None
        if "error" in json_aa and json_aa["error"] is not None:
            aa_error = ActionAttemptError(
                type=json_aa["error"]["type"],
                message=json_aa["error"]["message"],
            )

        if not wait_for_action_attempt or aa_error:
            return ActionAttempt(
                action_attempt_id=json_aa["action_attempt_id"],
                status=json_aa["status"],
                action_type=json_aa["action_type"],
                result=json_aa["result"],
                error=aa_error,
            )

        updated_action_attempt = self.seam.action_attempts.poll_until_ready(
            json_aa["action_attempt_id"]
        )

        return updated_action_attempt
