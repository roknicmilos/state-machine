from enum import Enum
from typing import Callable

from base_sm import BaseStateMachine, Transition


class CameraState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    READY = "ready"
    STREAMING = "streaming"
    ERROR = "error"


class CameraEvent(Enum):
    CONNECT = "connect"
    CONNECT_OK = "connect_ok"
    START_STREAM = "start_stream"
    STOP_STREAM = "stop_stream"
    ERROR = "error"
    RESET = "reset"


class CameraSM(BaseStateMachine[CameraState, CameraEvent]):
    State = CameraState
    Event = CameraEvent

    def get_init_state(self) -> CameraState:
        return CameraState.DISCONNECTED

    def get_transitions(self) -> list[Transition[CameraState, CameraEvent]]:
        return [
            Transition(
                trigger_event=CameraEvent.CONNECT,
                from_state=CameraState.DISCONNECTED,
                to_state=CameraState.CONNECTING,
                action=self._init_camera,
                description="Begin connection",
            ),
            Transition(
                trigger_event=CameraEvent.CONNECT_OK,
                from_state=CameraState.CONNECTING,
                to_state=CameraState.READY,
                action=self._camera_ready,
                description="Connection established",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=CameraState.CONNECTING,
                to_state=CameraState.ERROR,
                action=self._handle_error,
                description="Connection failed",
            ),
            Transition(
                trigger_event=CameraEvent.START_STREAM,
                from_state=CameraState.READY,
                to_state=CameraState.STREAMING,
                action=self._start_stream,
                description="Start streaming",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=CameraState.READY,
                to_state=CameraState.ERROR,
                action=self._handle_error,
                description="Runtime error",
            ),
            Transition(
                trigger_event=CameraEvent.STOP_STREAM,
                from_state=CameraState.STREAMING,
                to_state=CameraState.READY,
                action=self._camera_ready,
                description="Stop streaming",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=CameraState.STREAMING,
                to_state=CameraState.ERROR,
                action=self._handle_error,
                description="Streaming error",
            ),
            Transition(
                trigger_event=CameraEvent.RESET,
                from_state=CameraState.ERROR,
                to_state=CameraState.DISCONNECTED,
                action=self._cleanup,
                description="Reset from error",
            ),
        ]

    def get_state_actions(self) -> dict[CameraState, Callable[[], None]]:
        return {
            CameraState.CONNECTING: self._init_camera,
            CameraState.READY: self._camera_ready,
            CameraState.STREAMING: self._start_stream,
            CameraState.ERROR: self._handle_error,
            CameraState.DISCONNECTED: self._cleanup,
        }

    def _init_camera(self) -> None:
        print("> [action] Initializing...\n")

    def _camera_ready(self) -> None:
        print("> [action] Ready.\n")

    def _start_stream(self) -> None:
        print("> [action] Streaming...\n")

    def _handle_error(self) -> None:
        print("> [action] Handling Error!\n")

    def _cleanup(self) -> None:
        print("> [action] Cleaning Up...\n")
