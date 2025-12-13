from enum import Enum

from base_sm import BaseStateMachine, Transition


class SensorState(Enum):
    DISCONNECTED = "disconnected"
    READY = "ready"
    MEASURING = "measuring"
    ERROR = "error"


class SensorEvent(Enum):
    CONNECT_OK = "connect_ok"
    START_MEASURE = "start_measure"
    STOP_MEASURE = "stop_measure"
    ERROR = "error"
    RESET = "reset"


class PressureSensorSM(BaseStateMachine):
    State = SensorState
    Event = SensorEvent

    def get_init_state(self) -> SensorState:
        return SensorState.DISCONNECTED

    def get_transitions(self) -> list[Transition]:
        return [
            Transition(
                trigger_event=SensorEvent.CONNECT_OK,
                from_state=SensorState.DISCONNECTED,
                to_state=SensorState.READY,
                action=self._sensor_ready,
                description="Connected",
            ),
            Transition(
                trigger_event=SensorEvent.START_MEASURE,
                from_state=SensorState.READY,
                to_state=SensorState.MEASURING,
                action=self._start_measuring,
                description="Begin measurement",
            ),
            Transition(
                trigger_event=SensorEvent.ERROR,
                from_state=SensorState.READY,
                to_state=SensorState.ERROR,
                action=self._handle_error,
                description="Sensor error",
            ),
            Transition(
                trigger_event=SensorEvent.STOP_MEASURE,
                from_state=SensorState.MEASURING,
                to_state=SensorState.READY,
                action=self._sensor_ready,
                description="Stop measurement",
            ),
            Transition(
                trigger_event=SensorEvent.ERROR,
                from_state=SensorState.MEASURING,
                to_state=SensorState.ERROR,
                action=self._handle_error,
                description="Measurement error",
            ),
            Transition(
                trigger_event=SensorEvent.RESET,
                from_state=SensorState.ERROR,
                to_state=SensorState.DISCONNECTED,
                action=self._cleanup,
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
