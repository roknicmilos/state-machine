from enum import Enum

from camera_sm import CameraSM, CameraEvent
from pressure_sensor_sm import PressureSensorSM, SensorEvent
from core import BaseStateMachine
from utils import log_event


def _handle_event(state_machine: BaseStateMachine, event: Enum) -> None:
    action_results, transition = state_machine.handle_event(event)
    log_event(
        sm_name=state_machine.name,
        event_name=event.name,
        action_results=action_results,
        transition=transition
    )


if __name__ == "__main__":
    print("############ Simulate CAMERA lifecycle ############")
    camera = CameraSM()
    print(f"Initial camera state: {camera.state.name}\n")
    _handle_event(camera, CameraEvent.CONNECT)
    _handle_event(camera, CameraEvent.CONNECT_OK)
    _handle_event(camera, CameraEvent.START_STREAM)
    _handle_event(camera, CameraEvent.STREAMING)
    _handle_event(camera, CameraEvent.STREAMING)
    _handle_event(camera, CameraEvent.STREAMING)
    _handle_event(camera, CameraEvent.STOP_STREAM)
    _handle_event(camera, CameraEvent.ERROR)
    _handle_event(camera, CameraEvent.RESET)

    print("- - - - - - - - - - - - - - - - - - - - - - - -\n")

    print("############ Simulate PRESSURE SENSOR lifecycle ############")
    sensor = PressureSensorSM()
    print(f"Initial sensor state: {sensor.state.name}\n")
    _handle_event(sensor, SensorEvent.CONNECT_OK)
    _handle_event(sensor, SensorEvent.START_MEASURE)
    _handle_event(sensor, SensorEvent.STREAMING)
    _handle_event(sensor, SensorEvent.STREAMING)
    _handle_event(sensor, SensorEvent.STREAMING)
    _handle_event(sensor, SensorEvent.STOP_MEASURE)
    _handle_event(sensor, SensorEvent.ERROR)
    _handle_event(sensor, SensorEvent.RESET)
