# state_machine

A lightweight, generic Python framework for building finite state machines (FSMs).

## Modules

- `BaseStateMachine` — abstract base class for all state machines.
- `Transition` — generic dataclass representing a state transition.

---

## Quick start

### 1. Define states and events

States and events are plain Python `Enum` classes:

```python
from enum import Enum


class DeviceState(Enum):
    OFFLINE = 'OFFLINE'
    READY = 'READY'
    ERROR = 'ERROR'


class DeviceEvent(Enum):
    POWER_ON = 'POWER_ON'
    ERROR = 'ERROR'
    RESET = 'RESET'
```

### 2. Define the state machine

Subclass `BaseStateMachine[StateType, EventType]` and implement `get_init_state`:

```python
from state_machine import BaseStateMachine


class DeviceStateMachine(BaseStateMachine[DeviceState, DeviceEvent]):
    def get_init_state(self) -> DeviceState:
        return DeviceState.OFFLINE
```

### 3. Define a `Transition` type for your device

You have two options, depending on how much static type-checking you want.

---

#### Option 1 — type alias (simple, less IDE support)

```python
from state_machine import Transition

DeviceTransition = Transition[DeviceState, DeviceEvent]
```

This is a runtime generic alias. It is concise and works correctly at runtime —
Pydantic enforces that `trigger_event` is a `DeviceEvent` and `source_state` /
`target_state` are `DeviceState` instances. However, most IDEs and static type
checkers (PyCharm, mypy, ty) **cannot resolve the concrete field types** through
a plain alias, so they will not warn you if you pass an incorrect type like a
plain string.

Use this approach when you prioritise brevity and are happy to rely on runtime
validation alone.

---

#### Option 2 — concrete subclass (recommended, full IDE support)

```python
from state_machine import Transition


class DeviceTransition(Transition[DeviceState, DeviceEvent]):
    """
    Represents a state transition in the device state machine.
    Fields trigger_event, source_state, and target_state are redefined here
    with specific types for better type checking and readability.
    """

    trigger_event: DeviceEvent
    source_state: DeviceState
    target_state: DeviceState
```

By redeclaring the fields with concrete types, IDEs and static type checkers see
exactly what types are expected. Passing a plain string such as
`trigger_event='POWER_ON'` instead of `DeviceEvent.POWER_ON` will be flagged
**before you run the code**.

Use this approach whenever you want early feedback from your IDE.

---

### 4. Register transitions and fire events

Transitions are registered on the state machine instance via `add_transition`.
Each transition accepts optional `before_callbacks` and `after_callbacks` —
plain callables that are invoked before and after the state change respectively.

```python
class DeviceController:
    def __init__(self) -> None:
        self.device_sm = DeviceStateMachine()
        self._register_transitions()

    def _register_transitions(self) -> None:
        self.device_sm.add_transition(
            DeviceTransition(
                trigger_event=DeviceEvent.POWER_ON,
                source_state=DeviceState.OFFLINE,
                target_state=DeviceState.READY,
                before_callbacks=[self._on_power_on],
            )
        )

        self.device_sm.add_transition(
            DeviceTransition(
                trigger_event=DeviceEvent.ERROR,
                source_state=DeviceState.READY,
                target_state=DeviceState.ERROR,
                before_callbacks=[self._on_error],
            )
        )

        self.device_sm.add_transition(
            DeviceTransition(
                trigger_event=DeviceEvent.RESET,
                source_state=DeviceState.ERROR,
                target_state=DeviceState.OFFLINE,
                after_callbacks=[self._on_reset],
            )
        )

    def _on_power_on(self) -> None:
        print('Powering on device.')

    def _on_error(self) -> None:
        print('Handling device error.')

    def _on_reset(self) -> None:
        print('Device reset complete.')

    def run(self) -> None:
        self.device_sm.handle_event(DeviceEvent.POWER_ON)
        self.device_sm.handle_event(DeviceEvent.ERROR)
        self.device_sm.handle_event(DeviceEvent.RESET)
```

---

## Transition callbacks

| Field | When it runs |
|---|---|
| `before_callbacks` | After the current state's exit, before `state` is updated |
| `after_callbacks` | After `state` is updated to `target_state` |

Both fields accept a list of zero-argument callables (`() -> None`).

---

## Duplicate transition guard

`add_transition` raises `ValueError` if you try to register two transitions with
the same `(source_state, trigger_event)` pair:

```python
# Second call raises:
# ValueError: Duplicate transition: a transition from
# <DeviceState.OFFLINE: 'OFFLINE'> with event <DeviceEvent.POWER_ON: 'POWER_ON'>
# is already defined.
device_sm.add_transition(DeviceTransition(...))  # first — OK
device_sm.add_transition(DeviceTransition(...))  # same source+event — raises
```

---

## Unhandled events

If `handle_event` is called with an event that has no registered transition from
the current state, it logs a warning and does nothing — it does **not** raise an
exception.
