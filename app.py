from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import redis
import os

# Tworzymy ręcznie mały zbiór treningowy
X_train = np.array([[1], [2], [3], [4], [5]])  # Przykładowe dane wejściowe
y_train = np.array([2, 4, 6, 8, 10])  # Odpowiednie wartości (y = 2*x)

# Tak jak w poprzednich przypadkach tworzymy model regresji liniowej
# i trenujemy go na stworzonych pwyżej danych
model = LinearRegression()
model.fit(X_train, y_train)


# Rozbudowujemy nasz serwer Flask o logikę walidacyjną
app = Flask(__name__)

# Pobranie zmiennej środowiskowej
api_key = os.getenv('API_KEY', 'default_api_key')  # 'default_api_key' to domyślna wartość, gdy zmienna nie jest ustawiona


@app.route('/')
def hello():
    return f"Hello, your API key is: {api_key}"


# Endpoint do predykcji
@app.route('/predict', methods=['POST'])
def predict():
    try:

        # Pobieramy dane wejściowe w formacie JSON
        data = request.get_json()

        # Sprawdzamy czy główny klucz istnieje
        if 'x' not in data:
            return jsonify({"error": "Brak wartości 'x' w żądaniu."}), 400

        # Sprawdzamy czy 'x' jest listą
        if not isinstance(data['x'], list):
            return jsonify({"error": "Wartość 'x' musi być listą liczb."}), 400

        # Sprawdzamy czy lista przekazanych wartości zawiera tylko liczby
        if not all(isinstance(i, (int, float)) for i in data['x']):
            return jsonify({"error": "Wartość 'x' może być tylko liczbą."}), 400

        # Pobieramy wartości i konwertujemy na tablicę 2D
        x_value = np.array(data['x']).reshape(-1, 1)
        # Dokonujemy predykcji wytrenowanym wcześniej modelem
        prediction = model.predict(x_value)

        # Zwracamy listę wyników predykcji
        return jsonify({"prediction": prediction.tolist()})

    # Obsługa innych błędów serwera
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint /info - Informacje o zbudowanym modelu
# Typ, ilość cech i rozmiar zbioru treningowego
@app.route('/info', methods=['GET'])
def model_info():
    info = {
        "model_type": "LinearRegression",
        "num_features": X_train.shape[1],
        "training_samples": len(X_train)
    }
    return jsonify(info)


# Endpoint /health - Zwracany status serwera
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


# Własna prosta dokumentacja
@app.route('/docs', methods=['GET'])
def docs():
    documentation = {
        "routes": {
            "/": "Strona główna API",
            "/predict": "POST - Przyjmuje JSON {x: [lista liczb]} i zwraca przewidywania",
            "/info": "GET - Zwraca informacje o modelu ML",
            "/health": "GET - Sprawdza status serwera",
            "/docs": "GET - Dokumentacja API",
            "/database": "GET - Redis cache"
        }
    }
    return jsonify(documentation)


# Dodatkowo połączenie z bazą danych redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.route('/database', methods=['GET'])
def cache_example():
    redis_client.set("example_key", "Hello from Redis!")
    value = redis_client.get("example_key")
    return jsonify({"cached_value": value})


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)