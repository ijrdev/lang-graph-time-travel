import streamlit as st
from graph.workflow import create_workflow, run_workflow_from_step

def main():
    st.title("Time Travel Workflow")
    
    # Sidebar para controles
    with st.sidebar:
        st.header("Controles")
        
        if st.button("Iniciar Workflow"):
            execution_id = start_new_execution()
            st.session_state["execution_id"] = execution_id
        
        # Time Travel
        if "execution_id" in st.session_state:
            snapshots = get_snapshots(st.session_state["execution_id"])
            
            selected_step = st.selectbox(
                "Voltar para step:",
                options=[s["step_name"] for s in snapshots]
            )
            
            if st.button("Time Travel"):
                run_workflow_from_step(
                    st.session_state["execution_id"], 
                    selected_step
                )
    
    # Área principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Estado Atual")
        if "current_state" in st.session_state:
            st.json(st.session_state["current_state"])
    
    with col2:
        st.header("Timeline")
        display_timeline()

def display_timeline():
    """Mostra timeline visual dos snapshots"""
    steps = ["observer", "query_builder", "search", "topic_generator", "content_generator"]
    
    for i, step in enumerate(steps):
        status = get_step_status(step)
        
        if status == "completed":
            st.success(f"✅ {step}")
        elif status == "current":
            st.info(f"🔄 {step}")
        else:
            st.empty()