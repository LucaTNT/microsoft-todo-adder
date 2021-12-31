import requests, json

class notifier:
    def __init__(self, bot_token, chat_id=None) -> None:
        self.bot_token = bot_token

        if chat_id:
            self.chat_id = chat_id
        pass

    def send_notification(self, text, chat_id: int =None) -> bool:
        chat_id = chat_id if chat_id else self.chat_id

        headers = {
            'Content-Type': 'application/json'
        }

        body = {
            'chat_id': chat_id,
            'text': text
        }

        try: 
            req = requests.post(f"https://api.telegram.org/bot{self.bot_token}/sendMessage", headers=headers, data=json.dumps(body))
            resp = req.json()

            return resp.get('ok') == True
        except Exception as e:
            raise
