from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load QA pipeline with TensorFlow backend
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad", framework="tf")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    question = data.get("question")
    context = data.get("context")
    result = qa_pipeline(question=question, context=context)
    return jsonify({
        "answer": result["answer"],
        "score": result["score"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
