# 🤖 AI-Powered Engineering Assistant
### Developed by Prajal Jain | 3rd Year AI Engineering Student

[![Streamlit App](https://static.streamlit.io/badges/streamlit-badge-svg)](https://share.streamlit.io/)

## 📌 Project Overview
This project is a **Serverless AI Chatbot** designed to provide intelligent responses for technical and general queries. Built as a part of my Cloud Computing portfolio, it demonstrates how to deploy Large Language Models (LLMs) using a "Lean Stack" that costs **$0 to host** while maintaining high performance.

## 🚀 Live Demo
🔗 **[Click here to chat with my AI]([REPLACE_WITH_YOUR_STREAMLIT_URL](https://my-ai-chatbot-hqdpyxpnpsrfrl89o5hywz.streamlit.app/))**

## 🛠️ Tech Stack
- **AI Brain:** `meta-llama/Meta-Llama-3-8B-Instruct` (Hugging Face Inference API)
- **Frontend:** Streamlit (Python Web Framework)
- **Cloud Infrastructure:** Streamlit Community Cloud
- **Version Control:** GitHub

## ✨ Key Features
- **Mechatronics Context:** Capable of assisting with Robotics, PLC, and Embedded Systems queries.
- **Session Memory:** Remembers context within a chat session for follow-up questions.
- **Secure Architecture:** Uses **Streamlit Secrets (TOML)** to protect API keys from public exposure.
- **High Scalability:** Handles multiple users using asynchronous cloud requests.

## 📖 How to Use
1. **Ask a Technical Question:** e.g., "Explain the difference between a PLC and a Microcontroller."
2. **Brainstorm Projects:** e.g., "Give me 5 AI ideas for a Mechatronics diploma student."
3. **Debug Code:** Paste a Python script and ask the AI to find errors.

## ⚙️ How to Run Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME

## install the necessary libraries:

pip install -r requirements.txt

## Set up your local secrets:

**Create a folder named .streamlit and a file inside it called secrets.toml.

**Add: HF_TOKEN = "your_huggingface_token_here"

##Start the app:


streamlit run app.py
