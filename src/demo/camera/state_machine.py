from enum import Enum

from state_machine import BaseStateMachine, Transition


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


class CameraTransition(Transition[CameraState, CameraEvent]):
    """
    Represents a state transition in the camera state machine.
    Fields trigger_event, source_state, and target_state are redefined here
    with specific types for better type checking and readability.
    """

    trigger_event: CameraEvent
    source_state: CameraState
    target_state: CameraState


class CameraStateMachine(BaseStateMachine[CameraState, CameraEvent]):
    """Simple camera device implemented as a state machine."""

    def get_init_state(self) -> CameraState:
        return CameraState.OFFLINE
