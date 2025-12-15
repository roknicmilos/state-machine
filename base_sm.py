from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

Action = Callable[[], str]


@dataclass
class State:
    name: str
    description: str | None = None
    on_event_actions: dict[Enum, list[Action]] = field(default_factory=dict)
    on_enter_actions: list[Action] = field(default_factory=list)
    on_exit_actions: list[Action] = field(default_factory=list)

    def on_event(self, event: Enum) -> list[str]:
        action_results = []
        actions = self.on_event_actions.get(event, [])
        for action in actions:
            action_results.append(f"on_event       > {action()}")
        return action_results

    def on_enter(self) -> list[str]:
        action_results = []
        for action in self.on_enter_actions:
            action_results.append(f"on_enter_state > {action()}")
        return action_results

    def on_exit(self) -> list[str]:
        action_results = []
        for action in self.on_exit_actions:
            action_results.append(f"on_exit_state  > {action()}")
        return action_results


@dataclass
class Transition:
    trigger_event: Enum
    from_state: State
    to_state: State
    actions: list[Action] = field(default_factory=list)
    description: str | None = None

    def on_trigger(self) -> list[str]:
        action_results = []
        for action in self.actions:
            action_results.append(f"on_transition  > {action()}")
        return action_results


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
        action_results = self.state.on_event(event)
        if transition := self.find_transition(self.state, event):
            action_results.extend(self.transition(transition))

        return action_results, transition

    def transition(self, transition: Transition) -> list[str]:
        """
        Perform actions associated with a state transition, and
        return the results of those actions.
        """
        action_results = [
            *self.state.on_exit(),
            *transition.on_trigger(),
        ]
        self.state = transition.to_state
        action_results.extend(self.state.on_enter())

        return action_results

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
