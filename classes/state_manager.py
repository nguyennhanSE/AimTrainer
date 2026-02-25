from enum import Enum


class GameState(Enum):
    START        = "start"
    PLAYING      = "playing"
    PAUSED       = "paused"
    RESULTS      = "results"
    INSTRUCTIONS = "instructions"
    SETTINGS     = "settings"
    MODE_SELECT  = "mode_select"
    STATISTICS   = "statistics"


class GameStateManager:

    def __init__(self, initial_state: GameState = GameState.START) -> None:
        self.current_state: GameState = initial_state

    def transition_to(self, state: GameState) -> None:
        if not isinstance(state, GameState):
            raise TypeError(f"Expected a GameState member, got {type(state)!r}.")
        self.current_state = state

    def is_state(self, state: GameState) -> bool:
        return self.current_state is state
