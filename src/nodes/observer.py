import logging

from src.states.main_state import MainState

def observer_node(state: MainState) -> MainState:
    try:
        logging.info("observer_node")
        
        return state
    except Exception as ex:
        raise ex
