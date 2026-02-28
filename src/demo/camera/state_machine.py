from enum import Enum

from state_machine import BaseStateMachine


class CameraState(Enum):
    OFFLINE = 'offline'
    READY = 'ready'
    STREAMING = 'streaming'
    ERROR = 'error'


class CameraEvent(Enum):
    POWER_ON = 'power_on'
    START_STREAM = 'start_stream'
    STOP_STREAM = 'stop_stream'
    ERROR = 'error'
    RESET = 'reset'


class CameraStateMachine(BaseStateMachine):
    """Simple camera device implemented as a state machine."""

    Event = CameraEvent

    def get_init_state(self) -> Enum:
        return CameraState.OFFLINE
