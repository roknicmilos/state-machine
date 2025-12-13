from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable


@dataclass
class Transition:
    trigger_event: Enum
    from_state: Enum
    to_state: Enum
    action: Callable[[], None] | None = None
    description: str | None = None


class BaseStateMachine(ABC):
    state: Enum
    transitions: list[Transition]

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.setup()

    def setup(self) -> None:
        self.state = self.get_init_state()
        self.transitions = self.get_transitions()

    @abstractmethod
    def get_init_state(self) -> Enum:
        ...

    @abstractmethod
    def get_transitions(self) -> list[Transition]:
        ...

    def handle_event(self, event: Enum) -> None:
        transition = self.find_transition(self.state, event)
        print(
            f"[{self.name}] 🔔 {event}: "
            f"🔄 {self.state.value} → {transition.to_state.value}"
        )
        self.state = transition.to_state

        if transition.action:
            transition.action()

    def find_transition(
        self,
        from_state: Enum,
        event: Enum
    ) -> Transition:
        for transition in self.transitions:
            if (
                transition.from_state == from_state and
                transition.trigger_event == event
            ):
                return transition

        raise Exception(
            f"[{self.name}] ❌ Invalid event '{event.value}' "
            f"for state {self.state.value}"
        )
