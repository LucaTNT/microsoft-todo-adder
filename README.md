# What is this
This tool exposes an HTTP endpoint that is used to easily add data to a Microsoft To Do list.
It was intended as an internal tool only, but I thought making it open source might be beneficial to someone.
I provide NO support, but you are free to use/edit it as you see fit.

# Basic info
Config is done through environment variables (see `config.py`)

POST to `/api/v1/todo` with the `Authorization header` set to whatever you have in `config.py` to send data to Microsoft Todo. You need to send a JSON payload like this:
`{"title": "The To Do Title", "note": "Your note"}`
