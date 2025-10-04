import logging

from datetime import datetime

from langgraph.graph.state import CompiledStateGraph
from langchain_community.tools import TavilySearchResults

from application.enums.status_enum import StatusEnum
from services.states.main_state import MainState
from infrastructure.repositories.subjects_repository import SubjectsRepository

def search_node(state: MainState, graph: CompiledStateGraph, config: dict) -> MainState:
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
        
        logging.info(f"🔍 search_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        graph_state = graph.get_state(config)
        
        SubjectsRepository.update(id = state.subject_id, checkpoint_id = graph_state.config["configurable"]["checkpoint_id"], status = StatusEnum.ERROR.value)
        
        raise ex
