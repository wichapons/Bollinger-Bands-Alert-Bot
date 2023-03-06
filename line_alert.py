import requests
from config import line_token


# function to send a Line API alert
def send_line_alert(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + line_token}
    payload = {"message": message}
    r = requests.post(url, headers=headers, data=payload)