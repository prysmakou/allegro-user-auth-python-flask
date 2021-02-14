# Allegro.pl user authenticator

## Purpose

Many Allegro API endpoints require bearer-token-for-user.
You can use this code to get the token for development purposes.
The application is a web server that has two routes:
* / - contains link to Allegro (sandbox)
* /auth - performs user authentication. Expects code (provided by Allegro) as http parameter.

## How to run

Initilize your python environment, eg:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install requirements:
```bash
pip install -r requirements.txt
```
Set environment variables with your Allegro application's data eg. by .env file:
```
cp .env-example .env
# Edit the file using your editor (I'm a VIMer)
vim .env
```
Important: import the environment variables:
```bash
source .env
```
Check if environment set ge by:
```bash
echo $ALLEGRO_CLIENT_APP_ID 
```
You should see the value of the variable (eg client id). Do not continue if the command returned empty line. It means you did something wrong! 

Start flack development server
```
flask run --host=0.0.0.0 --port=8000
```

Now go to your browser and enter server's url (eg "http://localhost:8000"). Then follow the link on the page.
You will be redirected to Allegro for authentication and autherisation of your client app to access your account.
After you authorise your app you you will be redirected back to this app. In case of success you will see JSON object with the 'token'.
You can use this token like this:
```bash
curl -sX GET "https://api.allegro.pl.allegrosandbox.pl/sale/offers" -H "authorization: Bearer <the token goes here>" -H 'accept: application/vnd.allegro.public.v1+json' 
```
More details on Allegro developer portal - https://developer.allegro.pl/auth/

## Troubleshooting
Sometimes using of "incognito" mode in browser helps.