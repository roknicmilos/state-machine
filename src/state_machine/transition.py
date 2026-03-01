from collections.abc import Callable
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Transition[StateType: Enum, EventType: Enum](BaseModel):
    """
    Represents a state transition in a state machine. Each transition is
    triggered by an event and defines the source and target states, as well as
    optional callbacks to perform before and after the transition.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, strict=True)

    trigger_event: EventType
    source_state: StateType
    target_state: StateType
    before_callbacks: list[Callable] = []
    after_callbacks: list[Callable] = []

    @property
    def display(self) -> str:
        """Return a string representation of the transition."""
        return (
            f'<source={self.source_state.value}; '
            f'event={self.trigger_event.value}; '
            f'target={self.target_state.value}>'
        )
