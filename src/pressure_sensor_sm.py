from enum import Enum

from core import BaseStateMachine, Transition, State


class SensorState(Enum):
    DISCONNECTED = "disconnected"
    READY = "ready"
    MEASURING = "measuring"
    ERROR = "error"


class SensorEvent(Enum):
    CONNECT_OK = "connect_ok"
    START_MEASURE = "start_measure"
    STREAMING = "streaming"
    STOP_MEASURE = "stop_measure"
    ERROR = "error"
    RESET = "reset"


class PressureSensorSM(BaseStateMachine):
    Event = SensorEvent

    def __init__(self):
        self.disconnected_state = State(
            name="disconnected",
            description="Sensor is disconnected.",
            on_enter_actions=[lambda: "Sensor disconnected."],
            on_exit_actions=[lambda: "Leaving disconnected state."],
        )
        self.ready_state = State(
            name="ready",
            description="Sensor is ready.",
            on_enter_actions=[lambda: "Sensor is now ready."],
            on_exit_actions=[lambda: "Sensor is no longer ready."],
        )
        self.measuring_state = State(
            name="measuring",
            description="Sensor is measuring.",
            on_event_actions={
                SensorEvent.STREAMING: [lambda: "Processing measurement..."]
            },
            on_enter_actions=[lambda: "Starting measurement."],
            on_exit_actions=[lambda: "Stopping measurement."],
        )
        self.error_state = State(
            name="error",
            description="Sensor encountered an error.",
            on_enter_actions=[lambda: "Entering error state."],
            on_exit_actions=[lambda: "Exiting error state."],
        )
        super().__init__()

    def get_init_state(self) -> State:
        return self.disconnected_state

    def get_transitions(self) -> list[Transition]:
        return [
            Transition(
                trigger_event=SensorEvent.CONNECT_OK,
                from_state=self.disconnected_state,
                to_state=self.ready_state,
                actions=[self._sensor_ready],
                description="Connected",
            ),
            Transition(
                trigger_event=SensorEvent.START_MEASURE,
                from_state=self.ready_state,
                to_state=self.measuring_state,
                actions=[self._start_measuring],
                description="Begin measurement",
            ),
            Transition(
                trigger_event=SensorEvent.ERROR,
                from_state=self.ready_state,
                to_state=self.error_state,
                actions=[self._handle_error],
                description="Sensor error",
            ),
            Transition(
                trigger_event=SensorEvent.STOP_MEASURE,
                from_state=self.measuring_state,
                to_state=self.ready_state,
                actions=[self._sensor_ready],
                description="Stop measurement",
            ),
            Transition(
                trigger_event=SensorEvent.ERROR,
                from_state=self.measuring_state,
                to_state=self.error_state,
                actions=[self._handle_error],
                description="Measurement error",
            ),
            Transition(
                trigger_event=SensorEvent.RESET,
                from_state=self.error_state,
                to_state=self.disconnected_state,
                actions=[self._cleanup],
                description="Reset sensor",
            ),
        ]

    def _sensor_ready(self) -> str:
        return "Ready."

    def _start_measuring(self) -> str:
        return "Measuring..."

    def _handle_error(self) -> str:
        return "Handling Error!"

    def _cleanup(self) -> str:
        return "Cleaning Up..."
