from camera_sm import CameraSM, CameraEvent

from pressure_sensor_sm import PressureSensorSM, SensorEvent

if __name__ == "__main__":
    print("############ Simulate CAMERA lifecycle ############")
    camera = CameraSM()
    print(f"Initial camera state: {camera.state.name}\n")
    camera.handle_event(CameraEvent.CONNECT)
    camera.handle_event(CameraEvent.CONNECT_OK)
    camera.handle_event(CameraEvent.START_STREAM)
    camera.handle_event(CameraEvent.STREAMING)
    camera.handle_event(CameraEvent.STREAMING)
    camera.handle_event(CameraEvent.STREAMING)
    camera.handle_event(CameraEvent.STOP_STREAM)
    camera.handle_event(CameraEvent.ERROR)
    camera.handle_event(CameraEvent.RESET)

    print("- - - - - - - - - - - - - - - - - - - - - - - -\n")

    print("############ Simulate PRESSURE SENSOR lifecycle ############")
    sensor = PressureSensorSM()
    print(f"Initial sensor state: {sensor.state.name}\n")
    sensor.handle_event(SensorEvent.CONNECT_OK)
    sensor.handle_event(SensorEvent.START_MEASURE)
    sensor.handle_event(SensorEvent.STREAMING)
    sensor.handle_event(SensorEvent.STREAMING)
    sensor.handle_event(SensorEvent.STREAMING)
    sensor.handle_event(SensorEvent.STOP_MEASURE)
    sensor.handle_event(SensorEvent.ERROR)
    sensor.handle_event(SensorEvent.RESET)
