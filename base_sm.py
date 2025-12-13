from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, TypeVar

State = TypeVar("State", bound=Enum)
Event = TypeVar("Event", bound=Enum)
TransactionsMap = dict[State, dict[Event, "Transition[State, Event]"]]


@dataclass
class Transition(Generic[State, Event]):
    trigger_event: Event
    target_state: State
    description: str | None = None


class BaseStateMachine(ABC, Generic[State, Event]):
    state: State | None

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.transitions_map: TransactionsMap = {}
        self.state_actions: dict[State, Callable[[], None]] = {}
        self.setup()

    def setup(self) -> None:
        self.set_initial_state(self.get_init_state())
        self.set_transitions_map(self.get_transitions_map())
        for state, action in self.get_state_actions().items():
            self.on_state(state, action)

    @abstractmethod
    def get_init_state(self) -> State:
        ...

    @abstractmethod
    def get_transitions_map(self) -> TransactionsMap:
        ...

    @abstractmethod
    def get_state_actions(self) -> dict[State, Callable[[], None]]:
        ...

    def set_initial_state(self, initial_state: State) -> None:
        self.state = initial_state

    def set_transitions_map(self, transitions: TransactionsMap) -> None:
        self.transitions_map = transitions

    def on_state(self, state: State, fn: Callable[[], None]) -> None:
        self.state_actions[state] = fn

    def trigger(self, event: Event) -> None:
        """
        Trigger a transition by event Enum from the current state.
        """
        if getattr(self, "state", None) is None:
            raise RuntimeError("Initial state not set!")

        events = self.transitions_map.get(self.state, {})

        if event not in events:
            # event is Enum — show its value for readability
            print(
                f"[{self.name}] ❌ Invalid event '{event.value}' "
                f"for state {self.state.value}"
            )
            return

        transition = events[event]
        print(
            f"[{self.name}] (🔔 {transition.trigger_event.value}) "
            f"🔄 {self.state.value} → {transition.target_state.value}"
        )
        self.state = transition.target_state

        if action := self.state_actions.get(transition.target_state):
            action()
