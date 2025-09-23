import sqlite3

from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from src.states.main_state import MainState
from src.nodes.observer import observer_node
from src.nodes.query_builder import query_builder_node
from src.nodes.search import search_node
from src.nodes.topics_generator import topics_generator_node
from src.nodes.content_generator import content_generator_node

class MainGraph():
    def __init__(self):
        self.sqlite_saver: SqliteSaver = SqliteSaver(sqlite3.connect("/data/db.db", check_same_thread = False))

        self.app: CompiledStateGraph = self._build_workflow()
        
    def run(self, data: dict, checkpoint_id: str | None = None) -> None:
        try:
            if checkpoint_id:
                self._resume_workflow_from_checkpoint(data["thread_id"], checkpoint_id)
            else:
                self._start_new_workflow(data["input"], data["thread_id"])
        except Exception as ex:
            raise ex

    def _build_workflow(self) -> CompiledStateGraph:
        try:
            workflow: StateGraph = StateGraph(MainState)
            
            workflow.add_node("observer", observer_node)
            workflow.add_node("query_builder", query_builder_node)
            workflow.add_node("search", search_node)
            workflow.add_node("topic_generator", topics_generator_node)
            workflow.add_node("content_generator", content_generator_node)
            
            workflow.set_entry_point("observer")
            workflow.add_edge("observer", "query_builder")
            workflow.add_edge("query_builder", "search")
            workflow.add_edge("search", "topic_generator")
            workflow.add_edge("topic_generator", "content_generator")
            workflow.set_finish_point("content_generator")
            
            return workflow.compile(checkpointer = self.sqlite_saver)
        except Exception as ex:
            raise ex

    def _resume_workflow_from_checkpoint(self, thread_id: str, checkpoint_id: str) -> None:
        try:
            print(f"Resumindo execução de um checkpoint_id: {checkpoint_id}.")
        
            # Nesse momento deve buscar no sqlite os dados do ckecpoint
            # E no final, atualizar a tabela dos assuntos.
            
            # Atualiza o checkpoint
            # config = graph.update_state(selected_state.config, values={"topic": "chickens"})
            config = {}
            
            self.app.invoke(None, config)
            
            print(f"Workflow concluído: {thread_id}.")
        except Exception as ex:
            raise ex
    
    def _start_new_workflow(self, input: str, thread_id: str) -> None:
        try:
            # Já cria o assunto na base com uma thread_id vinculada.
            
            print(f"Iniciando um novo workflow com a thread_id: {thread_id}.")
            
            self.app.invoke({"input": input}, {"configurable": {"thread_id": thread_id}})
            
            print(f"Workflow concluído: {thread_id}.")
        except Exception as ex:
            raise ex
