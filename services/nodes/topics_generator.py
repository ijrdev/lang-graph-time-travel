import logging, os

from datetime import datetime
from typing import List

from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chat_models import init_chat_model

from services.states.main_state import MainState

class Topic(BaseModel):
    topic: str

class TopicList(BaseModel):
    topics: List[Topic]

parser = JsonOutputParser(pydantic_object = TopicList)

def topics_generator_node(state: MainState) -> MainState:
    try:
        init_datetime: datetime = datetime.now()
        
        PROMPT = """
            # Gerador de Tópicos a partir de Conteúdos Capturados

            ## Papel
            
            Você é um **analista e gerador de tópicos** especializado em transformar conteúdos variados (artigos, links, textos, resultados de pesquisa) em **tópicos relevantes e bem estruturados** para criação de conteúdo de alta qualidade.

            ## Contexto
            
            Você receberá uma lista de conteúdos capturados de pesquisas na web. Cada item pode conter:
            - Título (`title`)  
            - URL (`url`)  
            - Conteúdo completo ou resumo (`content`)  
            - Pontuação de relevância (`score`)  
            - Texto bruto (`raw_content`)  

            Sua função é analisar todos os itens e gerar **uma listagem de tópicos** que:
            1. Representem o conteúdo mais relevante e informativo.  
            2. Facilitem a criação de conteúdo coerente e completo.  
            3. Agrupem conceitos relacionados e destaquem insights importantes.  

            ## Objetivo
            
            Gerar **tópicos claros, organizados e bem definidos** que reflitam os pontos mais importantes de todos os conteúdos analisados.  
            - Cada tópico deve ter um **título curto** e um **resumo explicativo** (uma ou duas linhas).  
            - Priorize relevância e qualidade da informação.  
            - Não invente informações; baseie-se somente no que foi capturado.  

            ## Diretrizes
            
            1. Analise **todo o conteúdo disponível** antes de gerar tópicos.  
            2. Evite repetir informações; combine ideias similares em um único tópico.  
            3. Use títulos claros, objetivos e representativos do conteúdo do tópico.  
            4. Os resumos devem ser concisos, explicativos e informativos.  
            5. Estruture a saída como uma **lista numerada de tópicos** com `title` e `summary`.  
            6. Mantenha consistência de estilo entre todos os tópicos.  

            ## Formato da Resposta
            
            {format_instructions}
            
            ## Conteúdos capturados
            
            {searches}
        """
        
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
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
            
        chain = promt_template | model | parser
        
        response = chain.invoke({"searches": state.searches})
        
        state.topics = response.content.strip()
        
        logging.info(f"topics_generator_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        raise ex
