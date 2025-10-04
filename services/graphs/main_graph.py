import sqlite3, logging

from pandas import DataFrame
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from application.enums.status_enum import StatusEnum
from services.states.main_state import MainState
from services.nodes.query_builder import query_builder_node
from services.nodes.search import search_node
from services.nodes.topics_generator import topics_generator_node
from services.nodes.content_generator import content_generator_node
from infrastructure.repositories.chekpoints_repository import CheckpointsRepository

class MainGraph():
    def __init__(self):
        self.sqlite_saver: SqliteSaver = SqliteSaver(sqlite3.connect("data/db.db", check_same_thread = False))

        self.config: dict = {}
        self.app: CompiledStateGraph = self._build_workflow()
        
    def run(self, data: dict) -> None:
        try:
            if data["status"] == StatusEnum.REPROCESS.value:
                df: DataFrame = CheckpointsRepository.get(data["checkpoint_id"], data["thread_id"])
                
                if len(df) == 0:
                    raise Exception("")
                
                checkpoint: list = df.to_dict("records")[0]
                
                self._resume_workflow(data["thread_id"], "checkpoint_id")
            elif data["status"] == StatusEnum.PENDING.value:
                self._start_workflow(data["subject"], data["thread_id"], data["id"])
            else:
                raise Exception(f"❌ Status ({data['status']}) do assunto ({data['subject']}) inválido para iniciar o processamento.")
        except Exception as ex:
            raise ex

    def _build_workflow(self) -> CompiledStateGraph:
        try:
            workflow: StateGraph = StateGraph(MainState)
            
            workflow.add_node("query_builder", lambda state: query_builder_node(state, self.app, self.config))
            workflow.add_node("search", lambda state: search_node(state, self.app, self.config))
            workflow.add_node("topic_generator", lambda state: topics_generator_node(state, self.app, self.config))
            workflow.add_node("content_generator", lambda state: content_generator_node(state, self.app, self.config))
            
            workflow.set_entry_point("query_builder")
            workflow.add_edge("query_builder", "search")
            workflow.add_edge("search", "topic_generator")
            workflow.add_edge("topic_generator", "content_generator")
            workflow.set_finish_point("content_generator")
            
            return workflow.compile(checkpointer = self.sqlite_saver)
        except Exception as ex:
            raise ex

    def _resume_workflow(self, thread_id: str, checkpoint_id: str) -> None:
        try:
            logging.info(f"Resumindo execução de um checkpoint_id: {checkpoint_id}.")
        
            # Nesse momento deve buscar no sqlite os dados do ckecpoint
            # E no final, atualizar a tabela dos assuntos.
            
            # Atualiza o checkpoint
            # config = graph.update_state(selected_state.config, values={"topic": "chickens"})
            config = {}
            
            self.app.invoke(None, config)
            
            logging.info(f"Workflow concluído: {thread_id}.")
        except Exception as ex:
            raise ex
    
    def _start_workflow(self, input: str, thread_id: str, subject_id: int) -> None:
        try:
            logging.info(f"🚀 Novo workflow com a thread_id: {thread_id}.")
            
            self.config = {"configurable": {"thread_id": thread_id}}
            self.app.invoke({"input": input, "subject_id": subject_id}, self.config)
            
            logging.info(f"✅ Workflow concluído: {thread_id}.")
        except Exception as ex:
            raise ex
