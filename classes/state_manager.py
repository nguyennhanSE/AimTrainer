"""
GameState enum and GameStateManager — central state-machine for the game.
"""

from enum import Enum


class GameState(Enum):
    """
    Enumeration of all high-level game states.

    Attributes:
        START:    The initial main-menu / title screen.
        PLAYING:  Active gameplay is in progress.
        PAUSED:   Gameplay is suspended; a pause overlay is shown.
        RESULTS:  The round has ended and the results screen is displayed.
    """

    START   = "start"
    PLAYING = "playing"
    PAUSED  = "paused"
    RESULTS = "results"


class GameStateManager:
    """
    Lightweight state machine that holds and transitions between
    :class:`GameState` values.

    Usage example::

        gsm = GameStateManager()
        gsm.transition_to(GameState.PLAYING)
        if gsm.is_state(GameState.PLAYING):
            ...
    """

    def __init__(self, initial_state: GameState = GameState.START) -> None:
        """
        Args:
            initial_state: The state to start in (defaults to ``START``).
        """
        self.current_state: GameState = initial_state

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def transition_to(self, state: GameState) -> None:
        """
        Move to a new state.

        Args:
            state: The :class:`GameState` to switch to.

        Raises:
            TypeError: If *state* is not a :class:`GameState` member.
        """
        if not isinstance(state, GameState):
            raise TypeError(f"Expected a GameState member, got {type(state)!r}.")
        self.current_state = state

    def is_state(self, state: GameState) -> bool:
        """
        Check whether the manager is currently in *state*.

        Args:
            state: The :class:`GameState` to test against.

        Returns:
            ``True`` if the current state matches *state*, else ``False``.
        """
        return self.current_state is state
