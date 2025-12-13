from camera_sm import CameraSM, CameraEvent

from pressure_sensor_sm import PressureSensorSM, SensorEvent

if __name__ == "__main__":
    print("Simulate CAMERA lifecycle:\n")
    camera = CameraSM()
    camera.trigger(CameraEvent.CONNECT)
    camera.trigger(CameraEvent.CONNECT_OK)
    camera.trigger(CameraEvent.START_STREAM)
    camera.trigger(CameraEvent.ERROR)
    camera.trigger(CameraEvent.RESET)

    print("- - - - - - - - - - - - - - - - - - - - - - - -\n")

    print("Simulate PRESSURE SENSOR lifecycle:\n")
    sensor = PressureSensorSM()
    sensor.trigger(SensorEvent.CONNECT_OK)
    sensor.trigger(SensorEvent.START_MEASURE)
    sensor.trigger(SensorEvent.STOP_MEASURE)
    sensor.trigger(SensorEvent.ERROR)
    sensor.trigger(SensorEvent.RESET)
