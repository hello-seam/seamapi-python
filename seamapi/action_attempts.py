from seamapi.types import (
    AbstractActionAttempts,
    ActionAttemptError,
    ActionAttempt,
    AbstractSeam as Seam,
    ActionAttemptId,
)
import time
import requests
from typing import Union


def to_action_attempt_id(action_attempt: Union[ActionAttemptId, ActionAttempt]) -> str:
    if isinstance(action_attempt, str):
        return action_attempt
    return action_attempt.action_attempt_id


class ActionAttempts(AbstractActionAttempts):
    """
    A class used to retreive action attempt data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : dict
        Initial seam class

    Methods
    -------
    get(action_attempt)
        Gets data about an action attempt
    poll_until_ready(action_attempt)
        Polls an action attempt until its status is 'success' or 'error'
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : dict
          Intial seam class
        """
        
        self.seam = seam

    def get(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        """Gets data about an action attempt.

        Parameters
        ----------
        action_attempt : str or dict
            Action attempt id or action attempt dict

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            An action attempt dict.
        """

        action_attempt_id = to_action_attempt_id(action_attempt)
        res = requests.get(
            f"{self.seam.api_url}/action_attempts/get",
            headers={"Authorization": f"Bearer {self.seam.api_key}"},
            params={"action_attempt_id": action_attempt_id},
        )
        if not res.ok:
            raise Exception(res.text)
        json_aa = res.json()["action_attempt"]
        error = None
        if "error" in json_aa and json_aa["error"] is not None:
            error = ActionAttemptError(
                type=json_aa["error"]["type"],
                message=json_aa["error"]["message"],
            )
        return ActionAttempt(
            action_attempt_id=json_aa["action_attempt_id"],
            status=json_aa["status"],
            action_type=json_aa["action_type"],
            result=json_aa["result"],
            error=error,
        )

    def poll_until_ready(
        self, action_attempt: Union[ActionAttemptId, ActionAttempt]
    ) -> ActionAttempt:
        """
        Polls an action attempt until its status is 'success' or 'error'.

        Parameters
        ----------
        action_attempt : str or dict
            Action attempt id or action attempt dict

        Returns
        ------
            An action attempt dict.
        """

        updated_action_attempt = None
        while (
            updated_action_attempt is None or updated_action_attempt.status == "pending"
        ):
            updated_action_attempt = self.get(action_attempt)
            time.sleep(0.25)
        return updated_action_attempt
