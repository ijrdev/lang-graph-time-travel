import logging

from src.states.main_state import MainState

def topics_generator_node(state: MainState) -> MainState:
    try:
        logging.info("topics_generator_node")
        
        return state
    except Exception as ex:
        raise ex
