#!/usr/bin/env python3
import getopt
import hashlib
import json
import socket
import sys,time
from threading import Thread

logfile = open('log.txt', "a",  encoding='utf-8')

SALT = 'MaRo'


def write_to_log(msg):
    logfile.write(msg + "\n")
    logfile.flush()


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(100)

    credential_table = {}

    try:
        with open('credentials.json') as cred_file:
            credential_table = json.load(cred_file)
    except FileNotFoundError:
        pass

    clients = []

    print(f"Server started on Port {port}")

    def client_connection(client_to_handle, client_addr):

        client_to_handle.settimeout(60.0)

        success = False

        display_name = ''

        try:
            while not success:
                message = client_to_handle.recv(2048).decode()
                if message == 'LOGIN':
                    print('login request received.')
                    client_to_handle.send('USER'.encode())
                    message = client_to_handle.recv(2048).decode()
                    display_name = message
                    pwd_entry = credential_table.get(message, None)
                    if pwd_entry:
                        client_to_handle.send('PW'.encode())
                        message = client_to_handle.recv(2048).decode()
pwd = hashlib.sha256(f"{SALT}{message}".encode('utf-8')).hexdigest()
                        if pwd_entry == pwd:
                            client_to_handle.send('OK'.encode())
                            success = True
                            print('login success.')
                        else:
                            client_to_handle.send('WRONG'.encode())
elif message == 'REGISTER':
    print('registration request received.')
    client_to_handle.send('USER'.encode())
    username = client_to_handle.recv(2048).decode()
    display_name = username
    pwd_entry = credential_table.get(username, None)
    if pwd_entry:
        client_to_handle.send('ALREADYTAKEN'.encode())
                    else:
                        client_to_handle.send('PW'.encode())
                        message = client_to_handle.recv(2048).decode()
                        pwd = hashlib.sha256(f"{SALT}{message}".encode('utf-8')).hexdigest()
                        credential_table[username] = pwd
                        with open('credentials.json', 'w') as cred_file:
                            json.dump(credential_table, cred_file)
                        client_to_handle.send('OK'.encode())
                        success = True
                        print('registration success.')

            clients.append(client)

            print(f"{display_name}<{addr[0]}:{addr[1]}> connected")
            write_to_log(f"{display_name}<{addr[0]}:{addr[1]}> connected")

        except socket.timeout:
            return

        client_to_handle.send("Connected to chatroom successfully!".encode())
        send_to_all(f"{display_name} connected", client_to_handle)
        while True:
            try:
                message = client_to_handle.recv(2048).decode()
                if message:
                    message = message.strip()
                    if message == 'quit':
                        disconnect(client_to_handle, client_addr, display_name)
                    else:
                        message_to_send = f"<{display_name}> {message}"
                        print(message_to_send)
                        write_to_log(message_to_send)
                        send_to_all(message_to_send, client_to_handle)
            except OSError:
                continue

    def send_to_all(message, sending_client):
        for c in clients:
            if c != sending_client:
                try:
                    c.send(message.encode())
                except OSError:
                    disconnect(c)
                    continue

    def disconnect(client_to_disconnect, client_addr='UNKNOWN', display_name = "UNKNOWN"):
        print(f"{display_name}<{client_addr[0]}:{client_addr[1]}> disconnected")
        write_to_log(f"{display_name}<{client_addr[0]}:{client_addr[1]}> disconnected")
        send_to_all(f"{display_name} disconnected", client_to_disconnect)
        client_to_disconnect.close()
        if client_to_disconnect in clients:
            clients.remove(client_to_disconnect)

    try:
        while True:
            client, addr = server_socket.accept()

            Thread(target=client_connection, args=(client, addr)).start()

    except KeyboardInterrupt:
        logfile.close()
        server_socket.close()
        pass


def main(argv):
    port = 0
    opts, args = getopt.getopt(argv, "p:", ["port="])
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = int(arg)
    start_server(port)


if __name__ == "__main__":
    main(sys.argv[1:])
