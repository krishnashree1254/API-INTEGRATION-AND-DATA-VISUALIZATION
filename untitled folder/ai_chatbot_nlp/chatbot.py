import json
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('punkt_tab')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Prepare data
words = []
classes = []
documents = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        documents.append((tokens, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w.isalnum()]
words = sorted(set(words))
classes = sorted(set(classes))

# Bag of words
def bag_of_words(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

# Predict intent
def predict_class(sentence):
    bow = bag_of_words(sentence)
    scores = []
    for i, intent in enumerate(classes):
        match_score = np.dot(bow, bag_of_words(" ".join(intents["intents"][i]["patterns"])))
        scores.append((intent, match_score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0][0]

# Get response
def get_response(tag):
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

# Main chat loop
print("🤖 Chatbot is ready! Type 'quit' to exit.")
while True:
    msg = input("You: ")
    if msg.lower() == "quit":
        break
    intent = predict_class(msg)
    response = get_response(intent)
    print(f"Bot: {response}")
