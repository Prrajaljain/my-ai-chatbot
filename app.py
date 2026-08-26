import os
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient

app = Flask(__name__, template_folder="templates")

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    api_key = os.environ.get("HF_TOKEN")
    if not api_key:
        return jsonify({
            "error": "Missing HF_TOKEN environment variable! Please add HF_TOKEN in Vercel Settings > Environment Variables."
        }), 400

    data = request.get_json() or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided."}), 400

    try:
        client = InferenceClient(MODEL_ID, token=api_key)
        formatted_messages = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role in ["user", "assistant", "system"] and content:
                formatted_messages.append({"role": role, "content": content})

        response = client.chat_completion(
            messages=formatted_messages,
            max_tokens=600
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"AI service response error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)