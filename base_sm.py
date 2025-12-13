from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, TypeVar

StateType = TypeVar("StateType", bound=Enum)
EventType = TypeVar("EventType", bound=Enum)


@dataclass
class Transition(Generic[StateType, EventType]):
    trigger_event: EventType
    from_state: StateType
    to_state: StateType
    action: Callable[[], None] | None = None
    description: str | None = None


class BaseStateMachine(ABC, Generic[StateType, EventType]):
    state: StateType
    transitions: list[Transition[StateType, EventType]]

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.setup()

    def setup(self) -> None:
        self.state = self.get_init_state()
        self.transitions = self.get_transitions()

    @abstractmethod
    def get_init_state(self) -> StateType:
        ...

    @abstractmethod
    def get_transitions(self) -> list[Transition[StateType, EventType]]:
        ...

    def handle_event(self, event: EventType) -> None:
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
        from_state: StateType,
        event: EventType
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
