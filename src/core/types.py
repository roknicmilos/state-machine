from typing import Callable

# For demo purposes, all actions return strings
# describing what they did. This allows logging
# of action results.
Action = Callable[[], str]
