from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

Action = Callable[..., str]


@dataclass
class State:
    name: str
    description: str | None = None
    on_enter_actions: list[Action] = field(default_factory=list)
    on_exit_actions: list[Action] = field(default_factory=list)


@dataclass
class Transition:
    trigger_event: Enum
    from_state: State
    to_state: State
    actions: list[Action] = field(default_factory=list)
    description: str | None = None


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

    def handle_event(self, event: Enum) -> None:
        transition = self.find_transition(self.state, event)
        self.state = transition.to_state

        action_results = []
        for action in transition.actions:
            action_results.append(action())

        print(
            f"[{self.name}]\n"
            f" 🔔 event:       {transition.trigger_event.value}\n"
            f" 🔄 transition:  {transition.from_state.name} "
            f"→ {transition.to_state.name}\n"
            f" 🎯 actions:      {' ; '.join(action_results)}\n"
            f" 📝 description: {transition.description}\n"
        )

    def find_transition(
        self,
        from_state: State,
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
            f"for state {self.state.name}"
        )
