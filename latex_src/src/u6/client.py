#!/usr/bin/env python3
import getopt
from PyInquirer import prompt, print_json
import socket
import sys
from threading import Thread


def start_client(address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(srv_socket):
        try:
            while True:
                new_message = sys.stdin.readline()
                srv_socket.send(new_message.encode())
                if new_message.strip() == 'quit':
                    server_socket.close()
                    quit()
                else:
                    sys.stdout.write("<You>")
                    sys.stdout.write(new_message)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            server_socket.close()
            pass

    server_socket.connect((address, port))

    questions = [
        {'type': 'list',
         'name': 'is_login',
         'message': 'Do you want to log in or register?',
         'choices': ['login', 'register'],
         'filter': lambda val: val == 'login'},
        {'type': 'input',
         'name': 'username',
         'message': 'Enter Username:'},
        {'type': 'password',
         'name': 'password',
         'message': 'Enter Password:'},

    ]

    success = False

    while not success:
        answers = prompt(questions)
        username = answers['username']
        password = answers['password']
        is_login = answers['is_login']

        if is_login:
            server_socket.send('LOGIN'.encode())
            resp = server_socket.recv(2048).decode()
            if resp == 'USER':
                server_socket.send(username.encode())
                resp = server_socket.recv(2048).decode()
                if resp == 'PW':
                    server_socket.send(password.encode())
                    resp = server_socket.recv(2048).decode()
                    if resp == 'OK':
                        success = True
                    else:
                        print('login data was wrong, try again')
else:
    server_socket.send('REGISTER'.encode())
    resp = server_socket.recv(2048).decode()
    if resp == 'USER':
        server_socket.send(username.encode())
        resp = server_socket.recv(2048).decode()
        if resp == 'PW':
            server_socket.send(password.encode())
            resp = server_socket.recv(2048).decode()
            if resp == 'OK':
                success = True
        elif resp == 'ALREADYTAKEN':
            print('username already taken, try another one.')
        else:
            print('error?', resp)

    Thread(target=send_msg, args=(server_socket,)).start()

    try:
        while True:
            try:
                message = server_socket.recv(2048).decode()
                if message:
                    print(message)
                else:
                    pass
            except OSError:
                quit()
    except KeyboardInterrupt:
        pass


def main(argv):
    port = 0
    address = ''
    opts, args = getopt.getopt(argv, "s:p:", ["srv=", "port="])
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = int(arg)
        if opt in ("-s", "--srv"):
            address = arg
    start_client(address, port)


if __name__ == "__main__":
    main(sys.argv[1:])
