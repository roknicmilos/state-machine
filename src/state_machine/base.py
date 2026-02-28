from abc import ABC, abstractmethod
from enum import Enum

from state_machine import Transition


class BaseStateMachine(ABC):
    def __init__(self) -> None:
        self.name: str = self.__class__.__name__
        self.transitions: list[Transition] = []
        self.state: Enum = self.get_init_state()

    @abstractmethod
    def get_init_state(self) -> Enum: ...

    def add_transition(self, transition: Transition) -> None:
        """
        Add a transition to the state machine. Raises an error if a transition
        with the same source state and trigger event already exists.
        """
        if self.find_transition(
            transition.source_state, transition.trigger_event
        ):
            raise ValueError(
                'Duplicate transition: a transition from '
                f'{transition.source_state!r} with event '
                f'{transition.trigger_event!r} is already defined.'
            )

        self.transitions.append(transition)

    def handle_event(self, trigger_event: Enum) -> None:
        """
        Perform the transition associated with the given event and the current
        state, if such a transition exists. If it doesn't exist, this method
        does nothing.
        """
        if transition := self.find_transition(self.state, trigger_event):
            self.perform_transition(transition)

    def perform_transition(self, transition: Transition) -> None:
        """
        Perform callbacks associated with a state transition and update the
        current state. This method assumes that the given transition is valid
        for the current state.
        """
        for before_callback in transition.before_callbacks:
            before_callback()

        self.state = transition.target_state

        for after_callback in transition.after_callbacks:
            after_callback()

    def find_transition(
        self, source_state: Enum, trigger_event: Enum
    ) -> Transition | None:
        """
        Find a transition based on a state and a trigger event. Returns
        None if no such transition exists.
        """
        for transition in self.transitions:
            if (
                transition.source_state == source_state
                and transition.trigger_event == trigger_event
            ):
                return transition

        return None
