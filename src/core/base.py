from abc import ABC, abstractmethod
from enum import Enum

from core import State, Transition


class BaseStateMachine(ABC):
    state: State
    transitions: list[Transition]

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.setup()

    def setup(self) -> None:
        self.state = self.get_init_state()
        self.transitions = self.get_transitions()

    @abstractmethod
    def get_init_state(self) -> State:
        ...

    @abstractmethod
    def get_transitions(self) -> list[Transition]:
        ...

    def handle_event(self, event: Enum) -> tuple[list[str], Transition | None]:
        """
        Perform actions associated with an event and a state
        transition, and return the results of those actions.
        """
        results = self.state.on_event(event)
        if transition := self.find_transition(self.state, event):
            results.extend(self.transition(transition))

        return results, transition

    def transition(self, transition: Transition) -> list[str]:
        """
        Perform actions associated with a state transition, and
        return the results of those actions.
        """
        results = [
            *self.state.on_exit(),
            *transition.on_trigger(),
        ]
        self.state = transition.to_state
        results.extend(self.state.on_enter())

        return results

    def find_transition(
        self,
        from_state: State,
        event: Enum
    ) -> Transition | None:
        for transition in self.transitions:
            if (
                transition.from_state == from_state and
                transition.trigger_event == event
            ):
                return transition

        return None
