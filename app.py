import streamlit as st
from agent import agent
import pandas as pd

st.set_page_config(page_title="AirSial AI Agent", page_icon="✈️")
st.title("✈️ AirSial - AI Operations Agent")
st.markdown("**Ask questions about incident data in plain English**")

# Sample questions
st.sidebar.markdown("### 🚀 Sample Questions:")
sample_questions = [
    "How many bird strikes occurred?",
    "What are the most common incident types?",
    "Show me high severity incidents",
    "Show all bird strike incidents with 'High' severity.",
    "Any turbulence-related injuries this quarter?",
    "List all Passenger Misconduct incidents and their outcomes.",
    "What types of incidents are most often 'Closed'?",
    "Compare open incidents between Q1 and Q3.",
    "List all incidents from the last 30 days.",
    "Any repeat incidents involving the same department?",
    "Who reported the last hydraulic failure?",
    "List all incidents with 'Under Investigation' status by reporter.",
    "Show all incidents from the Ground Handling department.",
    "Any incidents reported by Flight Operations in August?",
    "List incidents that occurred during refueling.",
    "Which departments have the most high-severity incidents?",
    "What is the average number of incidents per month?",
    "Which month had the highest number of incidents?",
    "List incidents that are still under investigation.",
    "How many incidents are currently open vs closed?"
]

for i, q in enumerate(sample_questions):
    if st.sidebar.button(q, key=f"btn_{i}"):
        st.session_state.question = q

# Main interface
question = st.text_input(
    "Ask your question:",
    value=getattr(st.session_state, 'question', ''),
    placeholder="e.g., How many bird strikes occurred?"
)

if st.button("Get AI Analysis") and question:
    with st.spinner("🤖 AI agent analyzing data..."):
        answer = agent.ask_question(question)

        st.subheader("💡 AI Analysis:")
        st.write(answer)

        # Show raw data for reference
        with st.expander("📊 View Raw Incident Data"):
            st.dataframe(agent.df)

# Quick stats
st.sidebar.markdown("### 📈 Quick Stats")
st.sidebar.metric("Total Incidents", len(agent.df))
st.sidebar.metric("High Severity", len(agent.df[agent.df['severity'] == 'High']))
st.sidebar.metric("Bird Strikes", len(agent.df[agent.df['type'] == 'Bird Strike']))
