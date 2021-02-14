import base64
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv(verbose=True)

app = Flask(__name__)


@app.route('/')
def index():
    allegro_auth_url = "{0}/auth/oauth/authorize?response_type=code&client_id={1}&redirect_uri={2}".format(
        os.environ['ALLEGRO_URL'], os.environ['ALLEGRO_CLIENT_APP_ID'], os.environ['AUTH_REDIRECT_URI'])
    return "<a href=\"" + allegro_auth_url + "\">Visit Allegro</a>"


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    code = request.args.get('code', '')
    url = "{0}/auth/oauth/token?grant_type=authorization_code&code={1}&redirect_uri={2}".format(
        os.environ['ALLEGRO_URL'], code, os.environ['AUTH_REDIRECT_URI'])
    auth_str = os.environ['ALLEGRO_CLIENT_APP_ID'] + \
        ":" + os.environ['ALLEGRO_CLIENT_APP_SECRET']
    headers = {
        'authorization': 'Basic {}'.format(base64.b64encode(str.encode(auth_str)).decode('ASCII'))
    }
    allegro_respone = requests.post(url, headers=headers)
    return allegro_respone.json() if allegro_respone.status_code == 200 else "error"


if __name__ == "__main__":
    app.runhost = ()
