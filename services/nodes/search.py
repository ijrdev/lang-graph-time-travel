import logging

from datetime import datetime

from langchain_community.tools import TavilySearchResults

from services.states.main_state import MainState

def search_node(state: MainState) -> MainState:
    try:
        init_datetime: datetime = datetime.now()
        
        tool = TavilySearchResults(
            max_results = 5,
            include_answer = True,
            include_raw_content = True,
            include_images = False,
            search_depth = "advanced"
        )
        
        state.searches = tool.invoke({'query': state.query_builder})
        
        logging.info(f"search_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        raise ex
