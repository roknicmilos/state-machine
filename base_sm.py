from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Generic, TypeVar

S = TypeVar("S", bound=Enum)


class BaseStateMachine(ABC, Generic[S]):

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.state: S | None = None

        self.transitions: dict[S, list[S]] = {}
        self.state_actions: dict[S, Callable] = {}

        self.setup()

    def setup(self) -> None:
        self.set_initial_state(self.get_init_state())
        self.set_transitions(self.get_transitions())
        for state, action in self.get_state_actions().items():
            self.on_state(state, action)

    @abstractmethod
    def get_init_state(self) -> S:
        ...

    @abstractmethod
    def get_transitions(self) -> dict[S, list[S]]:
        ...

    @abstractmethod
    def get_state_actions(self) -> dict[S, Callable]:
        ...

    def set_initial_state(self, initial_state: S) -> None:
        self.state = initial_state

    def set_transitions(self, transitions: dict[S, list[S]]) -> None:
        self.transitions = transitions

    def on_state(self, state: S, fn: Callable[[], None]) -> None:
        self.state_actions[state] = fn

    def change_state(self, new_state: S) -> None:
        if self.state is None:
            raise RuntimeError("Initial state not set!")

        allowed = self.transitions.get(self.state, [])

        if new_state not in allowed:
            print(
                f"[{self.name}] ❌ Invalid transition "
                f"{self.state.value} → {new_state.value}"
            )
            return

        print(f"[{self.name}] 🔄 {self.state.value} → {new_state.value}")
        self.state = new_state

        if action := self.state_actions.get(new_state):
            action()
