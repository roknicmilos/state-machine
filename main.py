from camera_sm import CameraSM

from pressure_sensore_sm import PressureSensorSM

if __name__ == "__main__":
    print("Simulate CAMERA lifecycle")
    camera = CameraSM()
    camera.change_state(CameraSM.State.CONNECTING)
    camera.change_state(CameraSM.State.READY)
    camera.change_state(CameraSM.State.STREAMING)
    camera.change_state(CameraSM.State.ERROR)
    camera.change_state(CameraSM.State.DISCONNECTED)

    print("\n")

    print("Simulate PRESSURE SENSOR lifecycle")
    sensor = PressureSensorSM()
    sensor.change_state(PressureSensorSM.State.READY)
    sensor.change_state(PressureSensorSM.State.MEASURING)
    sensor.change_state(PressureSensorSM.State.READY)
    sensor.change_state(PressureSensorSM.State.ERROR)
    sensor.change_state(PressureSensorSM.State.DISCONNECTED)
