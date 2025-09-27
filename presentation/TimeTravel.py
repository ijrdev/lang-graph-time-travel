import streamlit as st, pandas as pd, re, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from streamlit_modal import Modal

from infrastructure.repositories.subjects_repository import SubjectsRepository

# Configurations.

st.set_page_config(page_title = "LangGraph - Time Travel", page_icon = "📝", layout = "wide")

modal = Modal(
    title = "Adicionar o Assunto", 
    key = "insert-subject",
    padding = 20, 
    max_width = 600
)

# Session State.

# Data.

SubjectsRepository.create_table()

df = SubjectsRepository.get_all()

df = df.drop(columns = ["id"])

df["created_at"] = pd.to_datetime(df["created_at"])
df["created_at"] = df["created_at"].dt.strftime("%d/%m/%Y %H:%M:%S")

df["updated_at"] = pd.to_datetime(df["updated_at"])
df["updated_at"] = df["updated_at"].dt.strftime("%d/%m/%Y %H:%M:%S")

df = df.rename(columns = {
    "thread_id": "Thread",
    "checkpoint_id": "Checkpoint",
    "created_at": "Data de Criação",
    "updated_at": "Data de Atualização",
    "subject": "Assunto",
    "status": "Status"
})

# Body.

st.title("LangGraph - Time Travel")

if st.button("Adicionar"):
    modal.open()

if modal.is_open():
    with modal.container():
        st.text("Adicione o assunto para poder gerar o conteúdo!")
        
        with st.form("add_subject"):
            subject = re.sub(r'\s+', ' ', st.text_area("Assunto").strip())

            if st.form_submit_button("Adicionar"):
                if subject:
                    st.success("Assunto adicionado com sucesso!")
                    
                    SubjectsRepository.add(subject)
                    
                    modal.close()
                else:
                    st.error("O campo não pode estar vazio.")

st.dataframe(df)

# import streamlit as st
# from graph.workflow import create_workflow, run_workflow_from_step

# def main():
#     st.title("Time Travel Workflow")
    
#     # Sidebar para controles
#     with st.sidebar:
#         st.header("Controles")
        
#         if st.button("Iniciar Workflow"):
#             execution_id = start_new_execution()
#             st.session_state["execution_id"] = execution_id
        
#         # Time Travel
#         if "execution_id" in st.session_state:
#             snapshots = get_snapshots(st.session_state["execution_id"])
            
#             selected_step = st.selectbox(
#                 "Voltar para step:",
#                 options=[s["step_name"] for s in snapshots]
#             )
            
#             if st.button("Time Travel"):
#                 run_workflow_from_step(
#                     st.session_state["execution_id"], 
#                     selected_step
#                 )
    
#     # Área principal
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.header("Estado Atual")
#         if "current_state" in st.session_state:
#             st.json(st.session_state["current_state"])
    
#     with col2:
#         st.header("Timeline")
#         display_timeline()

# def display_timeline():
#     """Mostra timeline visual dos snapshots"""
#     steps = ["observer", "query_builder", "search", "topic_generator", "content_generator"]
    
#     for i, step in enumerate(steps):
#         status = get_step_status(step)
        
#         if status == "completed":
#             st.success(f"✅ {step}")
#         elif status == "current":
#             st.info(f"🔄 {step}")
#         else:
#             st.empty()