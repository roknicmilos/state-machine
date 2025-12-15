from dataclasses import dataclass, field
from enum import Enum

from core import State, Action


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
