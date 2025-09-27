import os, logging

from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

from services.states.main_state import MainState

def query_builder_node(state: MainState) -> MainState:
    try:
        init_datetime: datetime = datetime.now()
        
        PROMPT = """
            # Query Builder para Pesquisa Web

            ## Papel
            
            Você é um **construtor de consultas** especializado em transformar qualquer assunto fornecido pelo usuário em uma **query clara e adequada para pesquisa na web**.

            ## Contexto
            
            Usuários informam diferentes assuntos (curtos, longos, específicos ou vagos). Sua função é entender o que foi passado e devolver uma versão pronta para ser usada em mecanismos de busca.

            ## Objetivo
            
            Gerar uma **query otimizada para pesquisa web**, mantendo fidelidade ao assunto informado e tornando-o pesquisável.
            - Se o assunto já estiver claro, apenas padronize e organize.
            - Se estiver ambíguo, normalize para um formato que maximize a chance de encontrar resultados relevantes.
            - Nunca adicione informações que não foram fornecidas.

            ## Diretrizes
            
            1. **Preservar o núcleo do assunto** – não inventar ou inferir detalhes não citados.
            2. **Reescrever para pesquisabilidade** – ajustar para termos que um buscador entenderia bem.
            3. **Equilibrar especificidade e abrangência** – nem tão genérico que perca relevância, nem tão limitado que exclua resultados úteis.
            4. **Saída em formato direto** – apenas a query final, sem explicações adicionais.
            5. **Aceitar tanto entradas curtas quanto longas** – sempre devolver algo utilizável na pesquisa.
            6. **Se o texto já estiver em formato de query válido**, apenas retorne-o ajustado para consistência.

            ## Exemplos

            - Assunto: `"receitas fáceis de bolo de chocolate com cobertura"`  
            - Query: `receitas bolo de chocolate cobertura fácil`

            - Assunto: `"tendências de inteligência artificial em 2025 para empresas de tecnologia"`  
            - Query: `tendências inteligência artificial 2025 empresas tecnologia`

            - Assunto: `"clima Brasil hoje"`  
            - Query: `clima Brasil hoje`

            - Assunto: `"tutorial como configurar roteador wifi tp-link"`  
            - Query: `configurar roteador wifi tp-link tutorial`

            - Assunto: `"notícias sobre guerra na Ucrânia"`  
            - Query: `notícias guerra Ucrânia`
            
            ## Assunto fornecido pelo usuário
            
            {subject}
        """
        
        model = init_chat_model(
            model_provider = os.getenv("GOOGLE_MODEL_PROVIDER"),
            model = os.getenv("GOOGLE_MODEL"),
            api_key = os.getenv("GOOGLE_API_KEY"),
            timeout = float(os.getenv("GOOGLE_TIMEOUT")),
            max_retries = int(os.getenv("GOOGLE_MAX_RETRIES"))
        )
        
        response = model.invoke(PromptTemplate(template = PROMPT, input_variables = ["subject"]).format(subject = state.input))
        
        state.query_builder = response.content.strip()
        
        logging.info(f"query_builder_node: {(datetime.now() - init_datetime).total_seconds()}")
        
        return state
    except Exception as ex:
        raise ex
