import logging, os

from datetime import datetime
from typing import List

from pydantic import BaseModel
from langgraph.graph.state import CompiledStateGraph
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model

from application.enums.status_enum import StatusEnum
from services.states.main_state import MainState
from infrastructure.repositories.subjects_repository import SubjectsRepository

class Topic(BaseModel):
    topic: str

class TopicList(BaseModel):
    topics: List[Topic]

parser = JsonOutputParser(pydantic_object = TopicList)

PROMPT = """
    # Especialista em gerar tópicos a partir de conteúdos

    ## Contexto
    
    Você receberá uma lista de conteúdos variados (artigos, links, textos, resultados de pesquisa) capturados de pesquisas na web, onde cada item conterá:
    - Título (`title`);
    - URL (`url`);
    - Conteúdo completo ou resumo (`content`);
    - Pontuação de relevância (`score`);
    - Texto bruto (`raw_content`);
    
    ## Tarefa
    
    Sua função é analisar todos os itens e gerar **uma listagem de tópicos** que:
    1. Seja ordenado pelo conteúdo mais simples/base ao mais complexo/detalhado;
    2. Facilite a criação de conteúdo coerente e completo;
    3. Agrupe conceitos relacionados e destaquem insights importantes;
    
    ## Objetivo
    
    Gerar **tópicos claros, organizados e bem definidos** que reflitam os pontos mais importantes de todos os conteúdos analisados.
    - **Cada tópico deve ter obrigatoriamente um título curto**, onde a ideia é capturar a essência do assunto de forma concisa;  
    - Priorize relevância e qualidade da informação;
    - Use linguagem clara e objetiva;
    - Não invente informações, baseie-se somente no que foi capturado;
    - Evite tópicos muito amplos ou genéricos, foque em aspectos específicos e úteis;
    - Evite repetições e sobreposições;
    - Sua linguagem de saída é em inglês, mesmo que o conteúdo analisado esteja em outro idioma;
    - Gere entre 5 a 10 tópicos, dependendo da quantidade e diversidade do conteúdo analisado;

    ## Formato da Resposta
    
    {format_instructions}
    
    ## Conteúdos
    
    {searches}
"""

def topics_generator_node(state: MainState, graph: CompiledStateGraph, config: dict) -> MainState:
    try:
        init_datetime: datetime = datetime.now()
        
        model = init_chat_model(
            model_provider = os.getenv("GOOGLE_MODEL_PROVIDER"),
            model = os.getenv("GOOGLE_MODEL"),
            api_key = os.getenv("GOOGLE_API_KEY"),
            timeout = float(os.getenv("GOOGLE_TIMEOUT")),
            max_retries = int(os.getenv("GOOGLE_MAX_RETRIES"))
        )
        
        promt_template = PromptTemplate(
            template = PROMPT, 
            input_variables = ["searches"],
            partial_variables = {"format_instructions": parser.get_format_instructions()}
        )
            
        chain = promt_template | model | parser
        
        response = chain.invoke({"searches": state.searches})
        
        state.topics = response["topics"]
        
        logging.info(f"🎯 topics_generator_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        graph_state = graph.get_state(config)
        
        SubjectsRepository.update(id = state.subject_id, checkpoint_id = graph_state.config["configurable"]["checkpoint_id"], status = StatusEnum.ERROR.value)
        
        raise ex
