from flask import Flask, redirect, jsonify, request, session
from oauthlib import oauth2
from config import Config
from requests_oauthlib import OAuth2Session
import json, os
import microsoft_todo_adder
from hacky_telegram_notifier import notifier

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'random-secret-key-not-that-important-in-this-use-case-i-think'
    app.notifier = notifier(app.config.get('TELEGRAM_BOT_TOKEN'), app.config.get('TELEGRAM_CHAT_ID'))

    try:
        app.todo = microsoft_todo_adder.microsoft_todo_adder(app.config)
    except microsoft_todo_adder.MissingTokenFile:
        print('Missing token file')
        app.notifier.send_notification(f"microsoft-todo-adder: missing token file, please authenticate at: https://sys.easypodcast.it/microsoft-todo-adder/authmsaccount/{app.config.get('AUTH_SECRET')}")
    
    import logging
    import sys
    log = logging.getLogger('requests_oauthlib')
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.DEBUG)
    return app

app = create_app()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Required for insecure http redirect_url
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' # Required because offline_access (which is required
                                               # to get the refresh token as well as the access token)
                                               # is not present in the scope in the token response, so
                                               # requests_oauthlib complains


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

@app.errorhandler(404)
def not_found(e):
    e = InvalidAPIUsage("Unavailable", 404)
    return jsonify(e.to_dict()), e.status_code

# the AUTH_SECRET parameter is used to prevent unauthorized users to change the linked account
@app.route(f"/authmsaccount/{app.config.get('AUTH_SECRET')}/")
def auth_ms_account():
    oauth2 = OAuth2Session(app.config.get('CLIENT_ID'),
                        redirect_uri=app.config.get('REDIRECT_URI'),
                        scope=app.config.get('SCOPE'))
    session.clear()
    url, state = oauth2.authorization_url(app.config.get('AUTHORITY_URL') + app.config.get('AUTH_ENDPOINT'),
                                          access_type="offline",
                                          response_mode="query")

    session['state'] = state
    return redirect(url)

@app.route("/authmsaccount/callback")
def auth_ms_account_callback():
    oauth2 = OAuth2Session(app.config.get('CLIENT_ID'),
                        redirect_uri=app.config.get('REDIRECT_URI'),
                        scope=app.config.get('SCOPE'),
                        state=session.get('state'))

    """Handler for the application's Redirect Uri."""
    # redirected admin consent flow
    if request.args.get('error'):
        if request.args.get('error_subcode'):
            error_description = request.args.get('error_subcode')
        else:
            error_description = request.args['error_description']

        message = '<strong>Error:</strong> ' \
                + request.args['error'] \
                + '</br> <strong>Reason:</strong> ' \
                + error_description

        return message, 301

    if session.get('state') and str(session['state']) != str(request.args.get('state')):
        return 'state returned to redirect URL does not match!', 301

    token = oauth2.fetch_token(app.config.get('TOKEN_ENDPOINT_URL'),
                                include_client_id=True,
                                client_secret=app.config.get('CLIENT_SECRET'),
                                authorization_response=request.url,
                                scope=app.config.get('SCOPE'))

    with open(app.config.get('TOKEN_STORAGE_FILE'), 'w') as token_storage_file:
        json.dump(token, token_storage_file)

    return f'access token <pre>{token}</pre> saved'

@app.route('/api/v1/todo', methods=["POST"])
def add_todo():
    if request.headers.get('Authorization') != app.config.get('AUTH_SECRET'):
        raise InvalidAPIUsage('Unauthorized', 401)
        
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage("Invalid JSON provided!")

    return app.todo.create_task(data.get('title'), data.get('note', ''))

@app.route('/lists')
def whoami():
    return app.todo.get_lists()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
 