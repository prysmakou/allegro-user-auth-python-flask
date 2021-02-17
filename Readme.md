# Allegro.pl user authenticator

[Also see in Polish](Readme.PL.md)

## Purpose

Many Allegro API endpoints require bearer-token-for-user.
You can use this code to get the token for development purposes.
The application is a web server that has three routes:
* / - contains link to Allegro (sandbox)
* /auth - performs user authentication. Expects code (provided by Allegro) as http parameter.
* /refresh - refresh the token (after initial token obtained)

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

Start flack development server by eg:
```
flask run --host=0.0.0.0 --port=8000
```
### Getting user token
Now go to your browser and enter server's url (eg "http://localhost:8000"). Then follow the link on the page.
You will be redirected to Allegro for authentication and autherisation of your client app to access your account.
After you authorise your app you you will be redirected back to this app. In case of success you will see JSON object with the 'access_token'.
You can use this token like this:
```bash
curl -sX GET "https://api.allegro.pl.allegrosandbox.pl/sale/offers" -H "authorization: Bearer <the token goes here>" -H 'accept: application/vnd.allegro.public.v1+json' 
```
The respnse data also stored in 'data.json' file (for token refreshing purposes)

### Refreshing the token
If 'data.json' file found in file system you will be offered with the toking refreshing option. Remember, refreshing token valid for 30 days and stored in your filesystem so you do need run this server all the time. Just tart the server and refresh the token.

More details on Allegro developer portal - https://developer.allegro.pl/auth/

## Troubleshooting
Sometimes using of "incognito" mode in browser helps.