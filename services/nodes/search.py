import logging

from services.states.main_state import MainState

def search_node(state: MainState) -> MainState:
    try:
        logging.info("search_node")
        
        return state
    except Exception as ex:
        raise ex
