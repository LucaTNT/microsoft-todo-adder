from requests_oauthlib import OAuth2Session
import json

class MissingTokenFile(Exception):
    pass

class microsoft_todo_adder():
    def __init__(self, config):
        token_storage_file = config.get('TOKEN_STORAGE_FILE')
        client_id = config.get('CLIENT_ID')
        client_secret = config.get('CLIENT_SECRET')

        self.config = config

        try:
            with open(token_storage_file, 'r') as token_file:
                self.token = json.load(token_file)
        except:
            raise MissingTokenFile()

        extra = {
            'client_id': client_id,
            'client_secret': client_secret,
        }

        def token_updater(token):
            with open(token_storage_file, 'w') as token_file:
                self.token = json.dump(token, token_file)

        self.oauth2 = OAuth2Session(client_id,
                                    token=self.token,
                                    auto_refresh_kwargs=extra,
                                    auto_refresh_url=config.get('TOKEN_ENDPOINT_URL'),
                                    token_updater=token_updater)

    def whoami(self):
        return self.oauth2.get('https://graph.microsoft.com/v1.0/me').json()

    def get_lists(self):
        return self.oauth2.get(self.config.get('TODO_ENDPOINT') + "/lists").json()

    def create_task(self, title, note = ""):
        list_id = self.config.get("LIST_ID")

        task = {
            "title": title,
            "body": {
                "content": note,
                "contentType": "text"
            }
        }
        body = json.dumps(task)

        headers = {
            "Content-Type": "application/json"
        }

        req = self.oauth2.post(self.config.get('TODO_ENDPOINT') + f"/lists/{list_id}/tasks",
                               data=body,
                               headers=headers)

        return req.json()
