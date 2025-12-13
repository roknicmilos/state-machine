from enum import Enum
from typing import Callable

from base_sm import BaseStateMachine, Transition, TransitionsMap


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


class PressureSensorSM(BaseStateMachine[SensorState, SensorEvent]):
    State = SensorState
    Event = SensorEvent

    def get_init_state(self) -> SensorState:
        return SensorState.DISCONNECTED

    def get_transitions_map(self) -> TransitionsMap:
        return {
            SensorState.DISCONNECTED: {
                SensorEvent.CONNECT_OK: Transition(
                    target_state=SensorState.READY,
                    description="Connected"
                )
            },
            SensorState.READY: {
                SensorEvent.START_MEASURE: Transition(
                    target_state=SensorState.MEASURING,
                    description="Begin measurement"
                ),
                SensorEvent.ERROR: Transition(
                    target_state=SensorState.ERROR,
                    description="Sensor error"
                ),
            },
            SensorState.MEASURING: {
                SensorEvent.STOP_MEASURE: Transition(
                    target_state=SensorState.READY,
                    description="Stop measurement"
                ),
                SensorEvent.ERROR: Transition(
                    target_state=SensorState.ERROR,
                    description="Measurement error"
                ),
            },
            SensorState.ERROR: {
                SensorEvent.RESET: Transition(
                    target_state=SensorState.DISCONNECTED,
                    description="Reset sensor"
                )
            },
        }

    def get_state_actions(self) -> dict[SensorState, Callable[[], None]]:
        return {
            SensorState.READY: self._sensor_ready,
            SensorState.MEASURING: self._start_measuring,
            SensorState.ERROR: self._handle_error,
            SensorState.DISCONNECTED: self._cleanup,
        }

    def _sensor_ready(self) -> None:
        print("> [action] Ready.\n")

    def _start_measuring(self) -> None:
        print("> [action] Measuring...\n")

    def _handle_error(self) -> None:
        print("> [action] ERROR!\n")

    def _cleanup(self) -> None:
        print("> [action] Cleaning up...\n")
