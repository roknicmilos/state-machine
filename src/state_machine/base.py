from abc import ABC, abstractmethod
from enum import Enum

from state_machine import Transition
from utils import get_logger

logger = get_logger(__name__)


class BaseStateMachine(ABC):
    def __init__(self) -> None:
        self.name: str = self.__class__.__name__
        self.transitions: list[Transition] = []
        self.state: Enum = self.get_init_state()
        logger.info(f'{self.name} initialized with state {self.state.value}')

    @abstractmethod
    def get_init_state(self) -> Enum: ...

    def add_transition(self, transition: Transition) -> None:
        """
        Add a transition to the state machine. Raises an error if a transition
        with the same source state and trigger event already exists.
        """
        if self.find_transition(
            transition.source_state, transition.trigger_event
        ):
            raise ValueError(
                'Duplicate transition: a transition from '
                f'{transition.source_state!r} with event '
                f'{transition.trigger_event!r} is already defined.'
            )

        self.transitions.append(transition)

    def handle_event(self, trigger_event: Enum) -> None:
        """
        Perform the transition associated with the given event and the current
        state, if such a transition exists. If it doesn't exist, this method
        does nothing.
        """
        if transition := self.find_transition(self.state, trigger_event):
            self.perform_transition(transition)
        else:
            logger.warning(
                f'{self.name} has no transition from state {self.state.value} '
                f'with trigger event {trigger_event.value}'
            )

    def perform_transition(self, transition: Transition) -> None:
        """
        Perform callbacks associated with a state transition and update the
        current state. This method assumes that the given transition is valid
        for the current state.
        """
        transition_display = (
            f'<source={transition.source_state.value}; '
            f'event={transition.trigger_event.value}; '
            f'target={transition.target_state.value}>'
        )
        logger.info(f'{self.name} starting transition {transition_display}')
        for before_callback in transition.before_callbacks:
            before_callback()

        self.state = transition.target_state

        for after_callback in transition.after_callbacks:
            after_callback()

        logger.info(f'{self.name} completed transition {transition_display}')

    def find_transition(
        self, source_state: Enum, trigger_event: Enum
    ) -> Transition | None:
        """
        Find a transition based on a state and a trigger event. Returns
        None if no such transition exists.
        """
        for transition in self.transitions:
            if (
                transition.source_state == source_state
                and transition.trigger_event == trigger_event
            ):
                return transition

        return None
