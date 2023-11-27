import numpy as np
import joblib, os, random, string
from keras.models import load_model
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Define your model and tokenizer here
chatbot_model = load_model('model/model.h5')
tokenizer = joblib.load('model/tokenizer.pkl')
max_sequence_length = joblib.load('model/max_sequence_length.pkl')
le = joblib.load('model/le.pkl')
responses = joblib.load('model/responses.pkl')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    texts_p = []
    prediction_input = request.form['message']

    # Remove punctuation and convert to lowercase
    prediction_input = [letter.lower() for letter in prediction_input if letter not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    # Tokenize and pad the input
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], max_sequence_length)

    # Get the model's output prediction
    output = chatbot_model.predict(prediction_input)
    output = output.argmax()

    # Find the corresponding response based on the predicted tag
    response_tag = le.inverse_transform([output])[0]
    response = random.choice(responses[response_tag])

    return {'response': response}

if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000))