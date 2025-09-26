import logging

from services.states.main_state import MainState

def content_generator_node(state: MainState) -> MainState:
    try:
        logging.info("content_generator_node")
        
        return state
    except Exception as ex:
        raise ex
