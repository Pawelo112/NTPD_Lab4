# Uruchamianie aplikacji w trybie produkcyjnym

## 1. Uruchamianie aplikacji

### **1. Lokalnie**

Jeśli chcesz uruchomić aplikację na swoim komputerze bez Dockera:

1. **Upewnij się, że masz zainstalowanego Pythona (np. 3.9)**
2. **Zainstaluj wymagane biblioteki:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Uruchom aplikację Flask:**
   ```sh
   python app.py
   ```
4. **Dostępne endpointy:**
   - `http://127.0.0.1:5000/` – Strona główna
   - `http://127.0.0.1:5000/docs` – Dokumentacja
   - `http://127.0.0.1:5000/health` – Sprawdzenie statusu
   - `http://127.0.0.1:5000/info` – Informacje o stworzonym modelu ML
   - `http://127.0.0.1:5000/predict` – POST - Przyjmuje JSON {x: [lista liczb]} i zwraca predykcje
   - `http://127.0.0.1:5000/database` - Zwraca Redis cache
   

---
### **2. Za pomocą Dockera**

1. **Zbuduj obraz Dockera:**
   ```sh
   docker build -t flask-ml-app .
   ```
2. **Uruchom kontener:**
   ```sh
   docker run -p 5000:5000 flask-ml-app
   ```
3. **Sprawdzenie, czy działa:**
   ```sh
   http://127.0.0.1:5000/health
   ```
   Jeśli zwróci `{ "status": "ok" }`, to wszystko działa.

---

### **3. Za pomocą Docker Compose**

1. **Uruchom oba kontenery (Flask + Redis):**
   ```sh
   docker-compose up -d
   ```
2. **Sprawdź działające kontenery:**
   ```sh
   docker ps
   ```
3. **Przetestuj API:**
   - **Predykcja:**
     ```sh
     http://127.0.0.1:5000/predict
     ```
   - **Redis Cache:**
     ```sh
     http://127.0.0.1:5000/database
     ```

---

## 2. Konfiguracja aplikacji

### **Zmienne środowiskowe (do konfiguracji w `.env` lub Docker Compose)**

- `FLASK_ENV=production` – tryb produkcyjny
- `REDIS_HOST=redis` – host bazy danych Redis

### **Zasoby potrzebne do działania aplikacji**

- **Pamięć:** min. **512MB RAM**
- **Procesor:** min. **1 rdzeń CPU**
- **Dysk:** min. **100MB** dla Dockera




