# State Machine Framework

Small example project implementing **simple state machines framework** in
**Python**.

This framework includes/supports:

- **Abstract base class** for state machines,
- **Defining states** with entry and exit actions,
- **Defining transitions** between states with associated events and actions,
- **Handling events** to trigger state transitions.

Check out the code in [base_sm.py](./base_sm.py) for details.

## Demo

The project also includes a demo with **two example state machines**
demonstrating the framework:

- Camera connection lifecycle,
- Pressure sensor lifecycle.

See the "Quick start" section below to run the demo.

## Quick start

1. Ensure you have Python 3.8+ installed.

2. (Optional but recommended) Create and activate a virtual environment from the
   project root:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Run the demo script from the project root:
    ```bash
    python3 main.py
    ```

## What you should see

The script runs two small scenarios (camera and pressure sensor) and prints
transitions and actions, for example:

```
############ Simulate CAMERA lifecycle ############
Initial camera state: disconnected

[CameraSM]
 🔔 event:       connect
 🔄 transition:  disconnected → connecting
 🎯 action:      None
 📝 description: Begin connection

... (more transitions and actions)
```
