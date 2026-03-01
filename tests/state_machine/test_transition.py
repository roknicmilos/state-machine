"""Tests for Transition."""

import pytest
from pydantic import ValidationError

from state_machine import Transition
from tests.state_machine.conftest import Event, State


class TestTransitionCreation:
    """Tests covering instantiation and field validation of Transition."""

    def test_creates_with_required_fields(self) -> None:
        """
        Transition is created with correct values when all required fields are
        provided.
        """
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
        )
        assert t.trigger_event is Event.TO_B
        assert t.source_state is State.A
        assert t.target_state is State.B

    def test_before_callbacks_default_to_empty(self) -> None:
        """before_callbacks defaults to an empty list when not provided."""
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
        )
        assert t.before_callbacks == []

    def test_after_callbacks_default_to_empty(self) -> None:
        """after_callbacks defaults to an empty list when not provided."""
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
        )
        assert t.after_callbacks == []

    def test_accepts_before_and_after_callbacks(self) -> None:
        """Transition stores provided before and after callbacks correctly."""
        before = lambda: None  # noqa: E731
        after = lambda: None  # noqa: E731
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
            before_callbacks=[before],
            after_callbacks=[after],
        )
        assert t.before_callbacks == [before]
        assert t.after_callbacks == [after]

    def test_rejects_string_for_trigger_event(self) -> None:
        """
        Transition raises ValidationError when trigger_event is a plain string.
        """
        with pytest.raises(ValidationError):
            Transition[State, Event](
                trigger_event='TO_B',  # type: ignore[arg-type]
                source_state=State.A,
                target_state=State.B,
            )

    def test_rejects_string_for_source_state(self) -> None:
        """
        Transition raises ValidationError when source_state is a plain string.
        """
        with pytest.raises(ValidationError):
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state='A',  # type: ignore[arg-type]
                target_state=State.B,
            )

    def test_rejects_string_for_target_state(self) -> None:
        """
        Transition raises ValidationError when target_state is a plain string.
        """
        with pytest.raises(ValidationError):
            Transition[State, Event](
                trigger_event=Event.TO_B,
                source_state=State.A,
                target_state='B',  # type: ignore[arg-type]
            )


class TestTransitionDisplay:
    """Tests covering the display property of Transition."""

    def test_display_format(self) -> None:
        """
        display returns a formatted string with source, event, and target
        values.
        """
        t = Transition[State, Event](
            trigger_event=Event.TO_B,
            source_state=State.A,
            target_state=State.B,
        )
        assert t.display == '<source=A; event=TO_B; target=B>'
