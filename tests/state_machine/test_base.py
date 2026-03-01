"""Tests for BaseStateMachine."""

import pytest

from state_machine import BaseStateMachine, Transition
from tests.state_machine.conftest import Event, SimpleSM, State


class TestInitialization:
    """Tests covering state machine construction and initial state."""

    def test_initial_state_is_set(self, sm: SimpleSM) -> None:
        """State machine starts in the state returned by get_init_state."""
        assert sm.state is State.A

    def test_transitions_list_is_empty(self, sm: SimpleSM) -> None:
        """Transitions list is empty before any transitions are added."""
        assert sm.transitions == []

    def test_name_is_class_name(self, sm: SimpleSM) -> None:
        """name attribute equals the concrete subclass name."""
        assert sm.name == 'SimpleSM'

    def test_cannot_instantiate_without_get_init_state(self) -> None:
        """Instantiating BaseStateMachine directly raises TypeError."""
        with pytest.raises(TypeError):
            BaseStateMachine()  # type: ignore[abstract]


class TestAddTransition:
    """Tests covering add_transition, including duplicate detection."""

    def test_adds_transition(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """A valid transition is appended to the transitions list."""
        sm.add_transition(transition_a_to_b)
        assert len(sm.transitions) == 1

    def test_raises_on_duplicate_source_and_event(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """
        Adding a second transition with the same source and event raises
        ValueError.
        """
        sm.add_transition(transition_a_to_b)
        duplicate = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
        )
        with pytest.raises(ValueError, match='Duplicate transition'):
            sm.add_transition(duplicate)

    def test_allows_same_event_from_different_source(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """The same event can be registered from two different source states."""
        sm.add_transition(transition_a_to_b)
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.B,
            target_state=State.C,
        )
        sm.add_transition(t)
        assert len(sm.transitions) == 2

    def test_allows_same_source_with_different_event(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """Multiple events can be registered from the same source state."""
        sm.add_transition(transition_a_to_b)
        t = Transition[State, Event](
            trigger_event=Event.TO_C,
            source_state=State.A,
            target_state=State.C,
        )
        sm.add_transition(t)
        assert len(sm.transitions) == 2


class TestHandleEvent:
    """Tests covering event handling and state transitions."""

    def test_transitions_to_target_state(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """handle_event moves the machine to the transition's target state."""
        assert sm.state is State.A
        sm.add_transition(transition_a_to_b)
        sm.handle_event(Event.TO_B)
        assert sm.state is State.B

    def test_does_nothing_for_unregistered_event(
        self,
        sm: SimpleSM,
    ) -> None:
        """
        handle_event leaves state unchanged when no transition matches the
        event.
        """
        assert sm.state is State.A
        sm.handle_event(Event.UNKNOWN)
        assert sm.state is State.A

    def test_does_nothing_for_valid_event_in_wrong_state(
        self,
        sm: SimpleSM,
    ) -> None:
        """
        handle_event leaves state unchanged when the event is valid but not
        registered from the current state.
        """
        assert sm.state is State.A
        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_A,
                source_state=State.B,
                target_state=State.A,
            )
        )
        sm.handle_event(Event.TO_A)
        assert sm.state is State.A


class TestPerformTransition:
    """
    Tests covering callback execution order and state update in
    perform_transition.
    """

    def test_runs_before_callbacks_before_state_change(
        self, sm: SimpleSM
    ) -> None:
        """
        before_callbacks are invoked while the machine is still in the source
        state.
        """
        state_during_before: State | None = None

        def before() -> None:
            """Capture current state during before callback."""
            nonlocal state_during_before
            state_during_before = sm.state

        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state=State.A,
                target_state=State.B,
                before_callbacks=[before],
            )
        )
        sm.handle_event(Event.TO_B)
        assert state_during_before == State.A

    def test_runs_after_callbacks_after_state_change(
        self, sm: SimpleSM
    ) -> None:
        """
        after_callbacks are invoked after the machine has moved to the target
        state.
        """
        state_during_after: State | None = None

        def after() -> None:
            """Capture current state during after callback."""
            nonlocal state_during_after
            state_during_after = sm.state

        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state=State.A,
                target_state=State.B,
                after_callbacks=[after],
            )
        )
        sm.handle_event(Event.TO_B)
        assert state_during_after == State.B

    def test_runs_multiple_callbacks_in_order(self, sm: SimpleSM) -> None:
        """
        All before and after callbacks are called in the order they were
        registered.
        """
        order: list[str] = []
        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state=State.A,
                target_state=State.B,
                before_callbacks=[
                    lambda: order.append('before_1'),
                    lambda: order.append('before_2'),
                ],
                after_callbacks=[
                    lambda: order.append('after_1'),
                    lambda: order.append('after_2'),
                ],
            )
        )
        sm.handle_event(Event.TO_B)
        assert order == ['before_1', 'before_2', 'after_1', 'after_2']

    def test_chained_transitions(self, sm: SimpleSM) -> None:
        """
        Sequential events correctly move the machine through multiple states.
        """
        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state=State.A,
                target_state=State.B,
            )
        )
        sm.add_transition(
            Transition[State, Event](
                trigger_event=Event.TO_C,
                source_state=State.B,
                target_state=State.C,
            )
        )
        assert sm.state is State.A
        sm.handle_event(Event.TO_B)
        assert sm.state is State.B
        sm.handle_event(Event.TO_C)
        assert sm.state is State.C


class TestFindTransition:
    """Tests covering the internal _find_transition lookup."""

    def test_returns_transition_when_found(
        self,
        sm: SimpleSM,
        transition_a_to_b: Transition[State, Event],
    ) -> None:
        """_find_transition returns the matching transition object."""
        sm.add_transition(transition_a_to_b)
        found = sm._find_transition(State.A, Event.TO_B)
        assert found is transition_a_to_b

    def test_returns_none_when_not_found(self, sm: SimpleSM) -> None:
        """_find_transition returns None when no transition matches."""
        assert sm._find_transition(State.A, Event.TO_B) is None
