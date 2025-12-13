from enum import Enum

from base_sm import BaseStateMachine, Transition, State


class CameraEvent(Enum):
    CONNECT = "connect"
    CONNECT_OK = "connect_ok"
    START_STREAM = "start_stream"
    STOP_STREAM = "stop_stream"
    ERROR = "error"
    RESET = "reset"


class CameraSM(BaseStateMachine):
    Event = CameraEvent

    def __init__(self):
        self.disconnected_state = State(
            name="disconnected",
            description="Camera is disconnected.",
            on_enter_actions=[lambda: "Camera disconnected."],
            on_exit_actions=[lambda: "Connecting camera..."],
        )
        self.connected_state = State(
            name="connected",
            description="Camera is connected.",
            on_enter_actions=[lambda: "Camera connected successfully."],
            on_exit_actions=[lambda: "Disconnecting camera..."],
        )
        self.ready_state = State(
            name="ready",
            description="Camera is ready.",
            on_enter_actions=[lambda: "Camera is now ready."],
            on_exit_actions=[lambda: "Camera is no longer ready."],
        )
        self.streaming_state = State(
            name="streaming",
            description="Camera is streaming.",
            on_enter_actions=[lambda: "Starting camera stream."],
            on_exit_actions=[lambda: "Stopping camera stream."],
        )
        self.error_state = State(
            name="error",
            description="Camera encountered an error.",
            on_enter_actions=[lambda: "Entering error state."],
            on_exit_actions=[lambda: "Exiting error state."],
        )
        super().__init__()

    def get_init_state(self) -> State:
        return self.disconnected_state

    def get_transitions(self) -> list[Transition]:
        return [
            Transition(
                trigger_event=CameraEvent.CONNECT,
                from_state=self.disconnected_state,
                to_state=self.connected_state,
                actions=[self._init_camera],
                description="Begin connection",
            ),
            Transition(
                trigger_event=CameraEvent.CONNECT_OK,
                from_state=self.connected_state,
                to_state=self.ready_state,
                actions=[self._camera_ready],
                description="Connection established",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=self.connected_state,
                to_state=self.error_state,
                actions=[self._handle_error],
                description="Connection failed",
            ),
            Transition(
                trigger_event=CameraEvent.START_STREAM,
                from_state=self.ready_state,
                to_state=self.streaming_state,
                actions=[self._start_stream],
                description="Start streaming",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=self.ready_state,
                to_state=self.error_state,
                actions=[self._handle_error],
                description="Runtime error",
            ),
            Transition(
                trigger_event=CameraEvent.STOP_STREAM,
                from_state=self.streaming_state,
                to_state=self.ready_state,
                actions=[self._camera_ready],
                description="Stop streaming",
            ),
            Transition(
                trigger_event=CameraEvent.ERROR,
                from_state=self.streaming_state,
                to_state=self.error_state,
                actions=[self._handle_error],
                description="Streaming error",
            ),
            Transition(
                trigger_event=CameraEvent.RESET,
                from_state=self.error_state,
                to_state=self.disconnected_state,
                actions=[self._cleanup],
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
