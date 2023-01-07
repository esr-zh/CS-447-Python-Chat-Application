##CS 447 GROUP PROJECT BY ESRAH, MOHAMMAD, ILLYAR, WARDAH, RUZGAR 

import asyncio
import base64
import os
import argparse
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js
from pywebio.platform.tornado_http import start_server as start_http_server
from pywebio import start_server as start_ws_server
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100

password = b"my-secret-password"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000
)
key = base64.urlsafe_b64encode(kdf.derive(password))

# Use the key to create a Fernet object, which will be used to encrypt and decrypt messages
fernet = Fernet(key)

async def main():
    global chat_msgs
    defer_call(lambda: session_info.update(fernet=fernet))
    defer_call(lambda: session_info.update(salt=salt))
    
    put_markdown("## 🧊 Welcome to ZAGGU!\nOnline chatroom")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Enter chat", required=True, placeholder="Your name",
                           validate=lambda n: "This nickname is already taken!" if n in online_users or n == '📢' else None)

    online_users.add(nickname)
    encrypted_message = fernet.encrypt(f'`{nickname}` joined the chat!'.encode())
    chat_msgs.append(('📢', encrypted_message))
    msg_box.append(put_markdown(f'📢 `{nickname}` joined the chat'))
    refresh_task = run_async(refresh_msg(nickname, msg_box, fernet, salt))
    while True:
        data = await input_group("💭 New message", [
            input(placeholder="Message text ...", name="msg", id='input_msg'),
            actions(name="cmd", buttons=["Send", {'label': "Leave the chat", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Type your text!") if m["cmd"] == "Send" and not m['msg'] else None)

        if data is None:
            break

        encrypted_message = fernet.encrypt(data['msg'].encode())
        chat_msgs.append((nickname, encrypted_message))
        msg_box.append(put_markdown(f"`{nickname}`: {fernet.decrypt(encrypted_message).decode()}"))

    refresh_task.close()

    online_users.remove(nickname)
    toast("You left the chat!")
    msg_box.append(put_markdown(f'📢 User `{nickname}` left chat!'))
    encrypted_message = fernet.encrypt(f'User `{nickname}` left chat!'.encode())
    chat_msgs.append(('📢', encrypted_message))

    put_buttons(['Rejoin'], onclick=lambda btn: run_js('window.location.reload()'))

async def refresh_msg(nickname, msg_box, fernet, salt):
    global chat_msgs
    last_idx = len(chat_msgs)
    while True:
        await asyncio.sleep(1)
        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                decrypted_message = fernet.decrypt(m[1]).decode()
                msg_box.append(put_markdown(f"`{m[0]}`: {decrypted_message}"))
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()
    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)
    #start_server(main, debug=True, port=8080, cdn=False)
