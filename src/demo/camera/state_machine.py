from enum import Enum

from state_machine import BaseStateMachine


class CameraState(Enum):
    OFFLINE = 'OFFLINE'
    READY = 'READY'
    STREAMING = 'STREAMING'
    ERROR = 'ERROR'


class CameraEvent(Enum):
    POWER_ON = 'POWER_ON'
    START_STREAM = 'START_STREAM'
    STOP_STREAM = 'STOP_STREAM'
    ERROR = 'ERROR'
    RESET = 'RESET'


class CameraStateMachine(BaseStateMachine):
    """Simple camera device implemented as a state machine."""

    Event = CameraEvent

    def get_init_state(self) -> Enum:
        return CameraState.OFFLINE
