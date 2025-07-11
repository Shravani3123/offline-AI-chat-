from flask import Flask, request, render_template_string
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
chat_history_ids = None

HTML = """
<!doctype html>
<title>Offline Chatbot</title>
<h2>Chat with AI 🤖</h2>
<form method=post>
  <input type=text name=user_input autofocus>
  <input type=submit value=Send>
</form>
<pre>{{response}}</pre>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_history_ids
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
