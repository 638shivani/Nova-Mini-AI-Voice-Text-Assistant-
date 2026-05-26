from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
import joblib

# 1. Training Data (What you might say)
phrases = [
    # YouTube
    "open youtube", "play a song", "play shape of you on youtube", "play music", "start youtube",
    # Google
    "open google", "search google for", "look up something online", "google this for me",
    # Time
    "what time is it", "tell me the time", "current time", "do you have the time",
    # Joke
    "tell me a joke", "make me laugh", "say something funny", "joke",
    # Maps
    "open maps", "show me the map", "where am i", "google maps", "directions",
    # Calculator
    "open calculator", "math", "calculator", "i need to calculate",
    # Weather
    "what is the weather", "is it raining", "temperature outside", "weather forecast"
]

# 2. Labels (The exact intent names)
intents = [
    "open_youtube", "open_youtube", "open_youtube", "open_youtube", "open_youtube",
    "open_google", "open_google", "open_google", "open_google",
    "time", "time", "time", "time",
    "joke", "joke", "joke", "joke",
    "maps", "maps", "maps", "maps", "maps",
    "calculator", "calculator", "calculator", "calculator",
    "weather", "weather", "weather", "weather"
]

print("Training Intent Classifier...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(phrases)

clf = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)
clf.fit(X, intents)

joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(clf, 'intent_model.pkl')
print("Model trained and saved successfully! Your AI is smarter now.")