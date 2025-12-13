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

    def get_transitions_map(self) -> dict[
        CameraState, dict[CameraEvent, Transition[CameraState, CameraEvent]]]:
        return {
            CameraState.DISCONNECTED: {
                CameraEvent.CONNECT: Transition(
                    trigger_event=CameraEvent.CONNECT,
                    target_state=CameraState.CONNECTING,
                    description="Begin connection"
                )
            },
            CameraState.CONNECTING: {
                CameraEvent.CONNECT_OK: Transition(
                    trigger_event=CameraEvent.CONNECT_OK,
                    target_state=CameraState.READY,
                    description="Connection established"
                ),
                CameraEvent.ERROR: Transition(
                    trigger_event=CameraEvent.ERROR,
                    target_state=CameraState.ERROR,
                    description="Connection failed"
                ),
            },
            CameraState.READY: {
                CameraEvent.START_STREAM: Transition(
                    trigger_event=CameraEvent.START_STREAM,
                    target_state=CameraState.STREAMING,
                    description="Start streaming"
                ),
                CameraEvent.ERROR: Transition(
                    trigger_event=CameraEvent.ERROR,
                    target_state=CameraState.ERROR,
                    description="Runtime error"
                ),
            },
            CameraState.STREAMING: {
                CameraEvent.STOP_STREAM: Transition(
                    trigger_event=CameraEvent.STOP_STREAM,
                    target_state=CameraState.READY,
                    description="Stop streaming"
                ),
                CameraEvent.ERROR: Transition(
                    trigger_event=CameraEvent.ERROR,
                    target_state=CameraState.ERROR,
                    description="Streaming error"
                ),
            },
            CameraState.ERROR: {
                CameraEvent.RESET: Transition(
                    trigger_event=CameraEvent.RESET,
                    target_state=CameraState.DISCONNECTED,
                    description="Reset from error"
                )
            },
        }

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
        print("> [action] ERROR!\n")

    def _cleanup(self) -> None:
        print("> [action] Cleaning up...\n")
