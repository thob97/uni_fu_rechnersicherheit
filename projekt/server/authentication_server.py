import bcrypt
import pickle
import sys
import log_handler

sys_log = log_handler.sys_log
DATASIZE = 1024
credentials_file = 'system_files/credentials.file'
pepper = b'$2b$12$2MWTgbSl.nDtJghPIZe4f.'

def authenticate(client_socket, lock):
    #recv credentials
    try:
        login_or_create, username, password = client_socket.recv(DATASIZE).decode('utf-8').split('\t')
    #If client makes an input error (neither 0 or 1 for login or creationg)
    except ValueError:
        sys.exit('Authentication Error')

    #load credentials data
    try:
        with open(credentials_file, 'rb') as file:
            credentials_data = pickle.load(file)

    #if it doesent exists
    except:
        credentials_data = {}

    if login_or_create == 'login':
        #test if login credentials exist
        try:
            password_pepper = password.encode('utf-8') + pepper
            #Success
            if bcrypt.checkpw(password_pepper, credentials_data[username]):
                client_socket.sendall(b'1')
                sys_log.info(f'USER:{username}:LOGIN:success')
                #return data to server for further operations
                return username, password
            else:
                client_socket.sendall(b'Wrong credentials')
                sys_log.info(f'USER:{username}:LOGIN:wrong credentials')
                sys.exit(1)

        except KeyError:
            client_socket.sendall(b'Account does not exist')
            sys_log.info(f'USER:{username}:LOGIN:account does not exist')
            sys.exit(1)

    elif login_or_create == 'create':
        #lock because if 2 users create an account with the same username at the same time
        #one account will be overwritten
        with lock:
            try:
                #check if username is already in use
                credentials_data[username]
                client_socket.sendall(b'Username already in use, please try again')
                sys_log.info(f'USER:{username}:CREATE:username already taken')
                sys.exit(1)

            except KeyError:
                #hash password with pepper and salt
                password_pepper = password.encode('utf-8') + pepper
                hashed = bcrypt.hashpw(password_pepper, bcrypt.gensalt())

                #upload password hash and salt to credentials data
                credentials_data[username] = hashed

                #save updatet credentials
                with open(credentials_file, 'wb') as file:
                    pickle.dump(credentials_data, file)

                sys_log.info(f'USER:{username}:CREATE:success')

                #send success msg to client
                client_socket.sendall(b'1')

                #return data to server for further operations
                return username, password
    else:
        sys.exit('Authentication Error')
