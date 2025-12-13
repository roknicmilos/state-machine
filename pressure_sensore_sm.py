from enum import Enum
from typing import Callable

from base_sm import BaseStateMachine


class SensorState(Enum):
    DISCONNECTED = "disconnected"
    READY = "ready"
    MEASURING = "measuring"
    ERROR = "error"


class PressureSensorSM(BaseStateMachine[SensorState]):
    State = SensorState

    def get_init_state(self) -> SensorState:
        return SensorState.DISCONNECTED

    def get_transitions(self) -> dict[SensorState, list[SensorState]]:
        return {
            SensorState.DISCONNECTED: [SensorState.READY],
            SensorState.READY: [SensorState.MEASURING, SensorState.ERROR],
            SensorState.MEASURING: [SensorState.READY, SensorState.ERROR],
            SensorState.ERROR: [SensorState.DISCONNECTED],
        }

    def get_state_actions(self) -> dict[SensorState, Callable[[], None]]:
        return {
            SensorState.READY: self._sensor_ready,
            SensorState.MEASURING: self._start_measuring,
            SensorState.ERROR: self._handle_error,
        }

    def _sensor_ready(self) -> None:
        print("[Sensor] Ready.")

    def _start_measuring(self) -> None:
        print("[Sensor] Measuring...")

    def _handle_error(self) -> None:
        print("[Sensor] ERROR!")
