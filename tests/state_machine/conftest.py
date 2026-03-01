"""Shared fixtures for state_machine tests."""

from enum import Enum

import pytest

from state_machine import BaseStateMachine, Transition


class State(Enum):
    """Minimal state enum used across all state_machine tests."""

    A = 'A'
    B = 'B'
    C = 'C'


class Event(Enum):
    """Minimal event enum used across all state_machine tests."""

    TO_B = 'TO_B'
    TO_C = 'TO_C'
    TO_A = 'TO_A'
    UNKNOWN = 'UNKNOWN'


class SimpleSM(BaseStateMachine[State, Event]):
    """Minimal concrete state machine starting in State.A, used in tests."""

    def get_init_state(self) -> State:
        """Return the initial state."""
        return State.A


@pytest.fixture()
def sm() -> SimpleSM:
    """Return a fresh SimpleSM instance for each test."""
    return SimpleSM()


@pytest.fixture()
def transition_a_to_b() -> Transition[State, Event]:
    """Return a Transition from State.A to State.B triggered by Event.TO_B."""
    return Transition[State, Event](
        trigger_event=Event.TO_B,
        source_state=State.A,
        target_state=State.B,
    )
