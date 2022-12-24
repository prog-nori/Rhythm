import os
import base64

TOKEN = os.environ.get("TOKEN")

def get_token():
    if TOKEN is not None:
        decoded_token = base64.b64decode(TOKEN).decode()
        print('tkn:', decoded_token)
        return decoded_token
    else:
        return None