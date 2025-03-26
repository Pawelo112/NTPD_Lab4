# 1. Bazowy obraz Pythona (lekka wersja slim)
FROM python:3.9-slim

# 2. Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

# 3. Skopiowanie plików aplikacji do kontenera
COPY . .

# 4. Instalacja wymaganych bibliotek
RUN pip install --no-cache-dir -r requirements.txt

# 5. Eksponowanie portu, na którym działa aplikacja
EXPOSE 5000

# 6. Komenda do uruchomienia aplikacji przez Waitress (bo Gunicorn nie działa na Windowsie)
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "app:app"]
