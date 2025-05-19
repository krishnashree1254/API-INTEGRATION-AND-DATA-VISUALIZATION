# app.py
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)
model = joblib.load('spam_classifier.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    prediction = model.predict([message])[0]
    label = "Spam" if prediction == 1 else "Not Spam"
    return render_template('index.html', prediction_text=f'The message is: {label}')

if __name__ == '__main__':
    app.run(debug=True)
