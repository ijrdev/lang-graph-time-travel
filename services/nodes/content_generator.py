import logging, os

from datetime import datetime

from langgraph.graph.state import CompiledStateGraph
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.tools import TavilySearchResults

from application.enums.status_enum import StatusEnum
from services.states.main_state import MainState
from infrastructure.repositories.subjects_repository import SubjectsRepository

PROMPT = """
    # Escritor especialista em criar conteúdos informativos, bem estruturados e envolventes

    ## Contexto

    Você deve criar um conteúdo final completo baseando-se nos dados fornecidos.

    - Cada dado conterá um tópico e uma lista de conteúdos capturados da web relacionados a esse tópico;
        - Cada conteúdo terá título, URL, conteúdo completo ou resumo, pontuação de relevância e texto bruto;
        - Fique atento caso hava conteúdos que não façam sentido ou estejam corrompidos, neste caso, ignore-os;
    - Você deve analisar todos os conteúdos relacionados a cada tópico para criar um material coeso e informativo;
    - O conteúdo final deve ser dividido em seções claras, cada uma focada em um tópico específico;
    - Incorpore informações relevantes de cada conteúdo, garantindo que o texto flua naturalmente;

    ## Regras
    
    - Use linguagem clara, objetiva e envolvente;
    - Evite jargões técnicos, a menos que sejam essenciais para o entendimento;
    - Não invente informações, baseie-se somente no que foi capturado;
    - Use formatação adequada, como títulos, subtítulos, listas, ícones e parágrafos para melhorar a legibilidade;
    - Revise o texto para corrigir erros gramaticais e de digitação;
    - Sua linguagem de saída é unicamente em português (brasil), mesmo que o conteúdo analisado esteja em outro idioma;
    - Priorize qualidade e relevância da informação, focando em entregar valor ao leitor;
    - Seja criativo e original na abordagem do tema, tornando o conteúdo interessante e único;
    
    ## Exemplo do conteúdo da saída (obrigatoriamente deve ser em markdown)

    ```markdown
    # [Título Principal Atraente]

    ## Introdução
    [Parágrafo contextualizando o tema]

    ## [Tópico 1]
    [Desenvolvimento com pelo menos 1-3 parágrafos]

    ## [Tópico 2]
    [Desenvolvimento com pelo menos 1-3 parágrafos]

    ## [Tópico N]
    [Desenvolvimento com pelo menos 1-3 parágrafos]

    ## Conclusão
    [Síntese e reflexões finais]
    ```

    ## Dados

    {data}
"""

def content_generator_node(state: MainState, graph: CompiledStateGraph, config: dict) -> MainState:
    graph_state = graph.get_state(config)
    
    try:
        init_datetime: datetime = datetime.now()
        
        local_data_searches: list = []
        
        for item in state.topics:
            tool = TavilySearchResults(
                max_results = 1,
                include_answer = True,
                include_raw_content = True,
                include_images = False,
                search_depth = "advanced"
            )
            
            local_data_searches.append({"topic": item["topic"], "contents": tool.invoke({'query': item["topic"]})})
        
        model = init_chat_model(
            model_provider = os.getenv("GOOGLE_MODEL_PROVIDER"),
            model = os.getenv("GOOGLE_MODEL"),
            api_key = os.getenv("GOOGLE_API_KEY"),
            timeout = float(os.getenv("GOOGLE_TIMEOUT")),
            max_retries = int(os.getenv("GOOGLE_MAX_RETRIES"))
        )
        
        response = model.invoke(PromptTemplate(template = PROMPT, input_variables = ["data"]).format(data = local_data_searches))
        
        state.content = response.content.strip()
        
        SubjectsRepository.update(id = state.subject_id, checkpoint_id = graph_state.config["configurable"]["checkpoint_id"], status = StatusEnum.DONE.value)
        
        logging.info(f"📝 content_generator_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        SubjectsRepository.update(id = state.subject_id, checkpoint_id = graph_state.config["configurable"]["checkpoint_id"], status = StatusEnum.ERROR.value)
        
        raise ex
