from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


@dataclass
class Transition:
    """
    Represents a state transition in a state machine. Each transition is
    triggered by an event and defines the source and target states, as well as
    optional callbacks to perform before and after the transition.
    """

    trigger_event: Enum
    source_state: Enum
    target_state: Enum
    before_callbacks: list[Callable] = field(default_factory=list)
    after_callbacks: list[Callable] = field(default_factory=list)
