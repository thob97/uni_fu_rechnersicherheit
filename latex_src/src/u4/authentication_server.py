import bcrypt
import pickle
import socket 
import sys

DATASIZE = 1024
credentials_file = 'credentials.file'
pepper = b'$2b$12$2MWTgbSl.nDtJghPIZe4f.'

def authenticate(client_socket, lock):

    #recv credentials
    login_or_create, username, password = client_socket.recv(DATASIZE).decode('utf-8').split('\t')

    #load credentials data
    credentials_data = {}
    try:
        with open(credentials_file, 'rb') as file:
            credentials_data = pickle.load(file)
    except:
        pass

    if login_or_create == 'login':
        #test if login credentials exist
        try:
            password_pepper = password.encode('utf-8') + pepper
            #Success
            if bcrypt.checkpw(password_pepper, credentials_data[username]):
                client_socket.send(b'1')
                return 1
            else:
                client_socket.send(b'Wrong credentials')
                sys.exit()
        except:
            client_socket.send(b'Account does not exist')
            sys.exit()

    if login_or_create == 'create':
        #lock because if 2 users create an account with the same username at the same time
        #one account will be overwritten
        with lock:
            try:
                #check if username is already in use
                credentials_data[username]
                client_socket.send(b'Username already in use, please try again')
                sys.exit()

            except:
                #hash password with pepper and salt
                password_pepper = password.encode('utf-8') + pepper
                hashed = bcrypt.hashpw(password_pepper, bcrypt.gensalt())

                #upload password hash and salt to credentials data
                credentials_data[username] = hashed

                #save updatet credentials
                with open(credentials_file, 'wb') as file:
                    pickle.dump(credentials_data, file)

                #send success msg to client
                client_socket.send(b'1')
    else:
        raise Exception("An error in authentication has occurred")
