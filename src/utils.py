from base_sm import Transition


def log_event(
    sm_name: str,
    event_name: str,
    action_results: list[str],
    transition: Transition | None
) -> None:
    log = (
        f"[{sm_name}]\n"
        f" 🔔 event:       {event_name}\n"
    )
    if transition:
        log += (
            f" 🔄 transition:  {transition.from_state.name} "
            f"→ {transition.to_state.name}\n"
            f" 📝 description: {transition.description}\n"
        )
    else:
        log += " ⚠️  No valid transition found for this event.\n"

    if action_results:
        log += f" 🎯 actions: \n\t{'\n\t'.join(action_results)}\n"
    else:
        log += " 🎯 actions: None\n"

    print(log)
