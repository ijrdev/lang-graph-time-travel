import os, logging

from datetime import datetime

from langgraph.graph.state import CompiledStateGraph
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

from application.enums.status_enum import StatusEnum
from services.states.main_state import MainState
from infrastructure.repositories.subjects_repository import SubjectsRepository

PROMPT = """
    # Especialista em construir query otimizadas para pesquisa na web

    ## Contexto
    
    Usuários informam diferentes assuntos (curtos, longos, específicos, vagos, etc). Sua função é entender o que foi passado e devolver uma versão pronta para ser usada em mecanismos de busca.

    ## Diretrizes
    
    - Remova ambiguidades e termos vagos, faça o melhor para inferir a intenção e focar a query;
    - Se o assunto for muito específico, mantenha os detalhes essenciais para garantir relevância;
    - Priorize palavras que provavelmente trarão resultados úteis e relevantes;
    - Considere o uso de sinônimos ou palavras relacionados para ampliar a busca, se apropriado;
    - Adicione contexto temporal quando aplicável, por exemplo: "2024", "recente", "últimas novidades". Lembrando que a data atual é {current_date};
    - Se o assunto envolver múltiplos tópicos, tente focar nas partes mais relevantes ou combinar palavras de forma eficaz para a busca;

    ## Regras
    
    - Retorne APENAS a query otimizada, sem explicações adicionais;
    - Assuma que a busca é em inglês, a menos que a solicitação do usuário especifique outro idioma;
    - Evite repetir palavras desnecessariamente;
    - Não inclua aspas ou pontuação desnecessária na query;
    - Mantenha a query concisa usando idealmente entre 3-8 palavras;
    - Evite stop words desnecessáriosc como "o", "a", "de", etc, quando não agregam valor;
    
    ## Exemplos

    - Assunto: "Quero saber sobre as últimas novidades em inteligência artificial"
    - Query otimizada: inteligência artificial novidades 2025 tendências

    - Assunto: "Me explique como funciona a fotossíntese nas plantas"
    - Query otimizada: fotossíntese plantas processo funcionamento

    - Assunto: "Preciso de receitas saudáveis para o café da manhã"
    - Query otimizada: receitas café manhã saudáveis nutritivas

    - Assunto: "Quais são os melhores frameworks JavaScript para desenvolvimento web em 2025?"
    - Query otimizada: melhores frameworks JavaScript 2025 desenvolvimento web

    - Assunto: "Como investir em criptomoedas para iniciantes"
    - Query otimizada: investir criptomoedas iniciantes guia 2024
    
    ## Assunto fornecido pelo usuário
    
    {subject}
"""
        
def query_builder_node(state: MainState, graph: CompiledStateGraph, config: dict) -> MainState:
    try:
        init_datetime: datetime = datetime.now()
        
        model = init_chat_model(
            model_provider = os.getenv("GOOGLE_MODEL_PROVIDER"),
            model = os.getenv("GOOGLE_MODEL"),
            api_key = os.getenv("GOOGLE_API_KEY"),
            timeout = float(os.getenv("GOOGLE_TIMEOUT")),
            max_retries = int(os.getenv("GOOGLE_MAX_RETRIES"))
        )
        
        response = model.invoke(PromptTemplate(template = PROMPT, input_variables = ["subject"]).format(current_date = datetime.now().strftime("%Y-%m-%d")))
        
        state.query_builder = response.content.strip()
        
        logging.info(f"⚙️ query_builder_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        graph_state = graph.get_state(config)
        
        SubjectsRepository.update(id = state.subject_id, checkpoint_id = graph_state.config["configurable"]["checkpoint_id"], status = StatusEnum.ERROR.value)
        
        raise ex
