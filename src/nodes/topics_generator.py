from src.states.main_state import MainState

def topics_generator_node(state: MainState) -> MainState:
    try:
        return state
    except Exception as ex:
        raise ex
