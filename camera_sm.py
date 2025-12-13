from enum import Enum
from typing import Callable

from base_sm import BaseStateMachine


class CameraState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    READY = "ready"
    STREAMING = "streaming"
    ERROR = "error"


class CameraSM(BaseStateMachine[CameraState]):
    State = CameraState

    def get_init_state(self) -> CameraState:
        return CameraState.DISCONNECTED

    def get_transitions(self) -> dict[CameraState, list[CameraState]]:
        return {
            CameraState.DISCONNECTED: [CameraState.CONNECTING],
            CameraState.CONNECTING: [CameraState.READY, CameraState.ERROR],
            CameraState.READY: [CameraState.STREAMING, CameraState.ERROR],
            CameraState.STREAMING: [CameraState.READY, CameraState.ERROR],
            CameraState.ERROR: [CameraState.DISCONNECTED],
        }

    def get_state_actions(self) -> dict[CameraState, Callable]:
        return {
            CameraState.CONNECTING: self._init_camera,
            CameraState.READY: self._camera_ready,
            CameraState.STREAMING: self._start_stream,
            CameraState.ERROR: self._handle_error,
        }

    def _init_camera(self) -> None:
        print("[Camera] Initializing...")

    def _camera_ready(self) -> None:
        print("[Camera] Ready.")

    def _start_stream(self) -> None:
        print("[Camera] Streaming...")

    def _handle_error(self) -> None:
        print("[Camera] ERROR!")
