from enum import Enum

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


class CameraSM(BaseStateMachine):
    State = CameraState
    Event = CameraEvent

    def get_init_state(self) -> CameraState:
        return CameraState.DISCONNECTED

    def get_transitions(self) -> list[Transition]:
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

    def _init_camera(self) -> str:
        return "Initializing..."

    def _camera_ready(self) -> str:
        return "Ready."

    def _start_stream(self) -> str:
        return "Streaming..."

    def _handle_error(self) -> str:
        return "Handling Error!"

    def _cleanup(self) -> str:
        return "Cleaning Up..."
