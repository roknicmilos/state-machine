from dataclasses import dataclass, field
from enum import Enum

from core import Action


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
