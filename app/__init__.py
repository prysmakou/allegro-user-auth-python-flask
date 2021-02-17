import base64
import json
import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv(verbose=True)

app = Flask(__name__)
FILE_NAME = 'data.json'
AUTH_STRING = os.environ['ALLEGRO_CLIENT_APP_ID'] + \
    ":" + os.environ['ALLEGRO_CLIENT_APP_SECRET']

POST_HEADERS = {
    'authorization': 'Basic {}'.format(base64.b64encode(str.encode(AUTH_STRING)).decode('ASCII'))
}


def renew_token(refresh_token):
    url = "{0}/auth/oauth/token?grant_type=refresh_token&refresh_token={1}&redirect_uri={2}".format(
        os.environ['ALLEGRO_URL'], refresh_token, os.environ['AUTH_REDIRECT_URI'])
    allegro_response = requests.post(url, headers=POST_HEADERS)
    if allegro_response.status_code == 200:
        app.logger.debug('response: %s', allegro_response.json())
        app.logger.info(
            'Refreshing - token successefuly obtained. Saving to the file %s for renewal purposes', FILE_NAME)
        with open(FILE_NAME, 'w') as data_file:
            json.dump(allegro_response.json(), data_file)
        data = allegro_response.json()
    else:
        app.logger.error(
            'Error obtaining the token. Server responded with %s', allegro_response.status_code)
        data = ""
    return data


def get_renew_token_from_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data['refresh_token']


@app.route('/')
def index():
    html_content = ""
    if os.path.isfile(FILE_NAME):
        app.logger.info('Data file %s found', FILE_NAME)
        allegro_renew_url = "/refresh"
        html_content += "<p>Tokens found in the file storage.</p>" + "<p><a href=\"" + \
            allegro_renew_url + "\">Re-new user token from Allegro</a></p>"
    allegro_auth_url = "{0}/auth/oauth/authorize?response_type=code&client_id={1}&redirect_uri={2}".format(
        os.environ['ALLEGRO_URL'], os.environ['ALLEGRO_CLIENT_APP_ID'], os.environ['AUTH_REDIRECT_URI'])
    html_content += "<p><a href=\"" + allegro_auth_url + \
        "\">Request new user token from Allegro</a></p>"
    return html_content


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    html_content = ""
    code = request.args.get('code', '')
    url = "{0}/auth/oauth/token?grant_type=authorization_code&code={1}&redirect_uri={2}".format(
        os.environ['ALLEGRO_URL'], code, os.environ['AUTH_REDIRECT_URI'])
    allegro_response = requests.post(url, headers=POST_HEADERS)
    if allegro_response.status_code == 200:
        app.logger.info(
            'Token successefuly obtained. Saving to the file %s for renewal purposes', FILE_NAME)
        with open(FILE_NAME, 'w') as data_file:
            json.dump(allegro_response.json(), data_file)
        html_content = allegro_response.json()
    else:
        app.logger.error(
            'Error obtaining the token. Server responded with %s', allegro_response.status_code)
        html_content += "Error {}".format(allegro_response.status_code)
    return html_content


@app.route('/refresh')
def refresh():
    app.logger.debug("refresh token: %s", get_renew_token_from_file(FILE_NAME))
    data = renew_token(get_renew_token_from_file(FILE_NAME))
    html_content = data if data else 'Error'
    return html_content


if __name__ == "__main__":
    app.runhost = ()
