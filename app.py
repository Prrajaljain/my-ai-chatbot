"""
AI Engineering Assistant — Llama 3 via Hugging Face Inference API.

A Streamlit chat app with a mechatronics-focused system prompt. Conversation
history is kept in session state and truncated to the last N turns, so context
doesn't grow unbounded across a long chat and blow the token budget.

Local run:
    pip install -r requirements.txt
    mkdir -p .streamlit && echo 'HF_TOKEN = "hf_..."' > .streamlit/secrets.toml
    streamlit run app.py
"""

import streamlit as st
from huggingface_hub import InferenceClient

MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
MAX_TOKENS = 500
HISTORY_TURNS = 10  # messages sent back to the model, keeps context bounded

SYSTEM_PROMPT = """You are an engineering assistant specialising in mechatronics,
robotics, embedded systems and industrial automation.

Prefer concrete answers: name components, part numbers, pin mappings and real
values rather than describing things in general terms. When a question touches
hardware, mention the practical constraints that matter — current draw, timing,
thermal limits, mechanical tolerance.

If a question is outside engineering, answer it normally but briefly. Keep answers
tight; no filler preamble."""


st.set_page_config(page_title="AI Engineering Assistant | Prajal Jain", page_icon="🤖")
st.title("🤖 AI Engineering Assistant")
st.caption("Llama 3 8B Instruct · Streamlit · built by Prajal Jain")

# --- API access -------------------------------------------------------------- #

token = st.secrets.get("HF_TOKEN")
if not token:
    st.error(
        "Missing API key. Add `HF_TOKEN` under Settings → Secrets, or create "
        "`.streamlit/secrets.toml` locally."
    )
    st.stop()

client = InferenceClient(MODEL, token=token)

# --- Session state ----------------------------------------------------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About")
    st.write(
        "Engineering assistant tuned for mechatronics, robotics and embedded "
        "systems questions."
    )
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
    st.caption(f"Model: `{MODEL}`")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat -------------------------------------------------------------------- #


def build_payload(history: list[dict]) -> list[dict]:
    """System prompt plus the most recent turns, oldest of those first."""
    recent = history[-HISTORY_TURNS:]
    return [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": m["role"], "content": m["content"]} for m in recent
    ]


if prompt := st.chat_input("Ask an engineering question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Thinking..."):
                response = client.chat_completion(
                    messages=build_payload(st.session_state.messages),
                    max_tokens=MAX_TOKENS,
                )
            answer = response.choices[0].message.content
            placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as exc:  # noqa: BLE001 — surface the cause, don't swallow it
            placeholder.error("Request failed. Rate limit or model cold start — retry shortly.")
            with st.expander("Details"):
                st.code(f"{type(exc).__name__}: {exc}")
            # Drop the unanswered prompt so history stays consistent
            st.session_state.messages.pop()
