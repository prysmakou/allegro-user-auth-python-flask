# Allegro.pl - Autoryzacja użytkownika

Wiele punktów końcowych Allegro API wymaga bearer-token-for-user.
Możesz użyć tego kodu, aby uzyskać token do celów programistycznych.
Aplikacja jest serwerem WWW, który ma trzhy trasy:
* / - zawiera link do Allegro (piaskownica)
* /auth - przeprowadza autoryzację użytkownika. Oczekuje kodu (dostarczonego przez Allegro) jako parametru http.
* /refresh - przedłużenie ważności tokena (po uzyskaniu początkowego tokena)

## Jak używać

Zainicjuj swoje środowisko Pythona, np:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Zainstaluj wymagania:
```bash
pip install -r requirements.txt
```
Set environment variables with your Allegro application's data eg. by .env file:
```
cp .env-example .env
# Edit the file using your editor (I'm a VIMer)
vim .env
```

Start flack development server by eg:
```
flask run --host=0.0.0.0 --port=8000
```
### Uzyskanie początkowego tokena użytkownika
Przejdź do przeglądarki i wprowadź adres URL serwera (np. "http://localhost:8000"). Następnie kliknij łącze na stronie.
Zostaniesz przekierowany do Allegro w celu uwierzytelnienia i autoryzacji aplikacji klienckiej w celu uzyskania dostępu do konta.
Po autoryzacji aplikacji nastąpi przekierowanie z powrotem do tej aplikacji. W przypadku powodzenia zobaczysz obiekt JSON z 'access_token'.
Możesz użyć tego tokena w następujący sposób:
```bash
curl -sX GET "https://api.allegro.pl.allegrosandbox.pl/sale/offers" -H "authorization: Bearer <the token goes here>" -H 'accept: application/vnd.allegro.public.v1+json' 
```

### Przedłużenie ważności tokena
Jeśli plik "data.json" zostanie znaleziony w systemie plików, pojawi się opcja odświeżania toking. Pamiętaj, refresh token ważny przez 30 dni i przechowywany w twoim systemie plików, więc musisz cały czas uruchamiać ten serwer. Po prostu tartuj serwer i odśwież token.

Więcej szczegółów na temat Allegro - https://developer.allegro.pl/auth

