import streamlit as st
from huggingface_hub import InferenceClient

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Chatbot | Prajal Jain", page_icon="🤖")
st.title("🤖 My Student AI Assistant")
st.caption("Built with Llama 3 & Streamlit | Project by Prajal Jain")

# --- SECURE API ACCESS ---
# This looks for the 'Secret' you pasted in the Streamlit Settings
if "HF_TOKEN" in st.secrets:
    api_key = st.secrets["HF_TOKEN"]
else:
    st.error("Missing API Key! Go to Settings > Secrets and add HF_TOKEN.")
    st.stop()

# Initialize the AI 'Brain' (Llama 3 is free and very powerful)
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=api_key)

# --- CHAT HISTORY LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from the session
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT & AI RESPONSE ---
if prompt := st.chat_input("Ask me a question..."):
    # 1. Show the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate the AI's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # This calls the Hugging Face API for free
                response = client.chat_completion(
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    max_tokens=500
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("The AI is busy. Please wait 1 minute and try again!")
