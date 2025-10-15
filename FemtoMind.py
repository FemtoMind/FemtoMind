import streamlit as st
from smolagents import CodeAgent, OpenAIServerModel

st.set_page_config(page_title="FemtoMind", layout="wide")
st.title("Ask FemtoMind")

# -------------------------------
# Sidebar: API Key input
# -------------------------------
with st.sidebar:

    st.image("logo.png", width=200)

    #st.header("API Key")

    # Always use text_input; store in session_state if submitted
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.success("API key stored ✅")

    if st.button("Clear API Key"):
        if "api_key" in st.session_state:
            del st.session_state.api_key
        st.experimental_rerun()

# Stop if API key is missing
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.info("Please enter your Gemini API key in the sidebar to start chatting.")
    st.stop()



# -------------------------------
# Initialize Gemini model & agent
# -------------------------------
model = OpenAIServerModel(
    model_id="gemini-2.0-flash",  # Replace with valid model
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=st.session_state.api_key,
)


import numpy
import matplotlib
matplotlib.use("Agg")

agent = CodeAgent(tools=[], 
          model=model,
          additional_authorized_imports=["numpy", "matplotlib","matplotlib.pyplot"],
      )

# -------------------------------
# Initialize chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Display chat messages
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat input (must be at top-level)
# -------------------------------
prompt = st.chat_input("Say something")

if prompt:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.run(prompt)
            st.markdown(response)

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

