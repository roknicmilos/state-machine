from camera_sm import CameraSM, CameraEvent

from pressure_sensor_sm import PressureSensorSM, SensorEvent

if __name__ == "__main__":
    print("Simulate CAMERA lifecycle:\n")
    camera = CameraSM()
    camera.handle_event(CameraEvent.CONNECT)
    camera.handle_event(CameraEvent.CONNECT_OK)
    camera.handle_event(CameraEvent.START_STREAM)
    camera.handle_event(CameraEvent.ERROR)
    camera.handle_event(CameraEvent.RESET)

    print("- - - - - - - - - - - - - - - - - - - - - - - -\n")

    print("Simulate PRESSURE SENSOR lifecycle:\n")
    sensor = PressureSensorSM()
    sensor.handle_event(SensorEvent.CONNECT_OK)
    sensor.handle_event(SensorEvent.START_MEASURE)
    sensor.handle_event(SensorEvent.STOP_MEASURE)
    sensor.handle_event(SensorEvent.ERROR)
    sensor.handle_event(SensorEvent.RESET)
