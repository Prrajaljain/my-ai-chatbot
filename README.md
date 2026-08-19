# 🤖 AI Engineering Assistant

**A live chat assistant for mechatronics, robotics and embedded systems questions.**
Llama 3 8B Instruct via Hugging Face Inference API, deployed on Streamlit Community
Cloud at zero hosting cost.

### 🔗 [Try it — no signup](https://my-ai-chatbot-hqdpyxpnpsrfrl89o5hywz.streamlit.app/)

---

## 📌 What it is

A deployed web app, not a model. The interesting part isn't the LLM — it's the lean
stack: inference through a hosted API, a domain system prompt, session-scoped
memory, secrets-based key management, and a public URL that costs nothing to run.

Built to answer the kind of questions I actually have: PLC versus microcontroller
trade-offs, servo current draw, why an IMU drifts.

---

## 🛠️ Tech Stack

| Layer | Choice |
|---|---|
| Model | `meta-llama/Meta-Llama-3-8B-Instruct` |
| Inference | Hugging Face Inference API |
| Frontend | Streamlit |
| Hosting | Streamlit Community Cloud |
| Secrets | Streamlit Secrets (TOML) |

---

## ✨ Features

**Domain system prompt.** The model is instructed to prefer concrete answers —
component names, part numbers, pin mappings, real values — and to surface practical
hardware constraints like current draw and timing rather than describing concepts in
the abstract.

**Bounded context.** Session history is kept in `st.session_state` but only the last
10 turns are sent to the model. A long conversation otherwise grows the payload until
it hits the token limit and starts failing.

**Secrets, not literals.** The API token is read from Streamlit Secrets. Nothing
sensitive is in the repository.

**Honest error surfacing.** Failures show the exception type rather than a generic
"try again," so an auth problem is distinguishable from a rate limit. The unanswered
prompt is popped from history so state stays consistent.

---

## 📖 Try asking

- "Difference between a PLC and a microcontroller, and when each is the right call"
- "Why does an MPU6050 drift, and what filtering fixes it"
- "Five AI project ideas for a mechatronics student with a Raspberry Pi"
- Paste a Python traceback and ask what's wrong

---

## ⚙️ Run locally

```bash
git clone https://github.com/Prrajaljain/my-ai-chatbot.git
cd my-ai-chatbot
pip install -r requirements.txt
```

Add your Hugging Face token:

```bash
mkdir -p .streamlit
echo 'HF_TOKEN = "hf_your_token_here"' > .streamlit/secrets.toml
```

Get a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) — read access is enough.

```bash
streamlit run app.py
```

Opens at `localhost:8501`.

---

## 📂 Layout

```
app.py                    chat UI, system prompt, API call
requirements.txt          streamlit, huggingface_hub
README.md                 this file
.devcontainer/
└── devcontainer.json     Codespaces config — installs deps and auto-runs the app
```

## Notes

The free Inference API tier rate-limits and cold-starts, so the first request after
an idle period can take several seconds or fail once. Retrying works.

**One-click Codespaces.** The devcontainer installs dependencies and launches the
app automatically on attach, with port 8501 forwarded to a preview. Clone-and-run
with no local Python setup.
