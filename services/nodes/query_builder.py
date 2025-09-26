import logging

from services.states.main_state import MainState

def query_builder_node(state: MainState) -> MainState:
    try:
        logging.info("query_builder_node")
        
        return state
    except Exception as ex:
        raise ex
