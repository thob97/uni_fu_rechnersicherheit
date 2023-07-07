import sys

DATASIZE = 1024

def authenticate(server_socket):
    login_or_create = input("Enter 0 for login\nEnter 1 to create a new account: ")
    
    #login
    if(login_or_create == '0'):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        #tell server that clients wants to login
        response = f'login\t{username}\t{password}'
        server_socket.sendall(response.encode('utf-8'))
        #ask server if account matches credentials
        response = server_socket.recv(DATASIZE)

        #if successful
        if response == b'1':
            print('Success, you are logged in!')
            return 1

        else:
            print(response.decode('utf-8'))
            sys.exit()

    #create
    elif(login_or_create == '1'):
        username = input("Please enter a username: ")
        password = input("Please enter a password: ")

        #tell server that clients wants to create an account
        response = f'create\t{username}\t{password}'
        server_socket.sendall(response.encode('utf-8'))
        #ask server if account credentials are free
        response = server_socket.recv(DATASIZE)
        
        #if successful
        if response == b'1':
            print('Success, you are logged in!')
            return 1

        else:
            print(response.decode('utf-8'))
            sys.exit()

    else:
        print('Wrong Input')
        sys.exit()


