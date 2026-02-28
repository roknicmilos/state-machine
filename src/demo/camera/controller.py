from state_machine import Transition

from .state_machine import CameraStateMachine, CameraEvent, CameraState


class CameraController:
    """
    Orchestrates a CameraStateMachine by registering transitions and firing
    events.
    """

    def __init__(self) -> None:
        self.camera_sm = CameraStateMachine()
        self._register_transitions()

    def _register_transitions(self) -> None:
        self.camera_sm.add_transition(
            Transition(
                trigger_event=CameraEvent.POWER_ON,
                source_state=CameraState.OFFLINE,
                target_state=CameraState.READY,
                before_callbacks=[self._power_on],
            )
        )

        self.camera_sm.add_transition(
            Transition(
                trigger_event=CameraEvent.START_STREAM,
                source_state=CameraState.READY,
                target_state=CameraState.STREAMING,
                before_callbacks=[self._start_stream],
            )
        )

        self.camera_sm.add_transition(
            Transition(
                trigger_event=CameraEvent.STOP_STREAM,
                source_state=CameraState.STREAMING,
                target_state=CameraState.READY,
                before_callbacks=[self._stop_stream],
            )
        )

        for source_state in (
            CameraState.READY,
            CameraState.STREAMING,
        ):
            self.camera_sm.add_transition(
                Transition(
                    trigger_event=CameraEvent.ERROR,
                    source_state=source_state,
                    target_state=CameraState.ERROR,
                    before_callbacks=[self._handle_error],
                )
            )

        self.camera_sm.add_transition(
            Transition(
                trigger_event=CameraEvent.RESET,
                source_state=CameraState.ERROR,
                target_state=CameraState.OFFLINE,
                before_callbacks=[self._reset_device],
            )
        )

    # Callback implementations used as transition actions.

    def _power_on(self) -> str:
        return 'Powering on camera hardware.'

    def _start_stream(self) -> str:
        return 'Starting video stream.'

    def _stop_stream(self) -> str:
        return 'Stopping video stream.'

    def _handle_error(self) -> str:
        return 'Logging and handling camera error.'

    def _reset_device(self) -> str:
        return 'Resetting device to a safe offline state.'

    # Simple driver to trigger events and show state changes.

    def run_demo(self) -> None:
        sequence = [
            CameraEvent.POWER_ON,
            CameraEvent.START_STREAM,
            CameraEvent.ERROR,
            CameraEvent.RESET,
        ]

        for event in sequence:
            self.camera_sm.handle_event(event)
