
from src.states.main_state import MainState

def query_builder_node(state: MainState) -> MainState:
    try:
        return state
    except Exception as ex:
        raise ex
