import os

class Config(object):
    AUTHORITY_URL = os.environ.get('AUTHORITY_URL') or 'https://login.microsoftonline.com/consumers'
    AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
    TOKEN_ENDPOINT = '/oauth2/v2.0/token'

    AUTH_ENDPOINT_URL = AUTHORITY_URL + AUTH_ENDPOINT
    TOKEN_ENDPOINT_URL = AUTHORITY_URL + TOKEN_ENDPOINT

    TODO_ENDPOINT = "https://graph.microsoft.com/v1.0/me/todo"

    SCOPE = os.environ.get('SCOPE') or ["offline_access", "User.Read", "Tasks.ReadWrite.Shared", "Tasks.ReadWrite", "Tasks.Read", "Tasks.Read.Shared"]
    REDIRECT_URI = os.environ.get('REDIRECT_URI') or "http://localhost:5001/authmsaccount/callback"

    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    LIST_ID = os.environ.get('LIST_ID') or 'AQMkADAwATMwMAItYzc1OC0zZmE4LTAwAi0wMAoALgAAA4yKtcNqC_tJuFfULJvAWbYBAIPlbT47mmxFrlHqZPm8sFAAAss4k7wAAAA='

    AUTH_SECRET = os.environ.get('AUTH_SECRET') or 'supersecret'

    TOKEN_STORAGE_FILE = os.environ.get('TOKEN_STORAGE_FILE') or 'token.json'

    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
