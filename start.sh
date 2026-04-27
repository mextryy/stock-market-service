#!/bin/bash

# 1. Sprawdzenie, czy użytkownik podał numer portu
if [ -z "$1" ]
then
    echo "Błąd: Nie podano numeru portu."
    echo "Użycie: ./start.sh [PORT]"
    echo "Przykład: ./start.sh 8080"
    exit 1
fi

# 2. Przypisanie pierwszego argumentu ($1) do zmiennej PORT
export PORT=$1

echo "Uruchamiam Stock market service na porcie: $PORT..."

# 3. Uruchomienie docker-compose
# --build wymusza przebudowanie obrazu (ważne, gdy zmienisz coś w kodzie Pythona)
docker-compose up --build