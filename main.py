from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

apikey = os.getenv("GROQ_API_KEY")
client = Groq(api_key = apikey)

app = Flask(__name__)   
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')
    
    response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Act like a helpful personal assistant."},
                    {"role": "user",   "content": question}
                ],
                temperature=0.7,
                max_tokens=512
            )
    
    answer = response.choices[0].message.content.strip()

    return jsonify({"response": answer})

@app.route('/summarise', methods=['POST'])
def summarise():
    email_text = request.form.get('email_text')
    prompt = f"Summarize the following email in 4-5 sentences:\n{email_text}"
    response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Act like an expert email assistant."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.3,
                max_tokens=512
            )
    summary = response.choices[0].message.content.strip()
    return jsonify({"response": summary})


if __name__ == '__main__':
    app.run(debug=True)