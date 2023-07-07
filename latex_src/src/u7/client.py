import socket
import threading
import authentication_client 
import commands_client 

IP = "0.0.0.0"
PORT = 1234
DATASIZE = 1024


#one incoming msg thread
def incoming_msg(server_socket):
    #while server_socket is alive
    while not server_socket._closed:
        #waits for msg from server of size DATASIZE
        msg = server_socket.recv(DATASIZE)
        #print msg
        print(msg.decode('utf-8'))

#one outgoing msg thread
def outgoing_msg(server_socket):
    #while server_socket is alive
    while not server_socket._closed:
        #wait for keyboard input
        msg = input()
        commands_client.handle_commands(msg, server_socket)

def main():
    #connect socket(IP4, tcp)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((IP,PORT))

    authentication_client.authenticate(server_socket)
    commands_client.print_available_commands()

    threading.Thread(target= incoming_msg, args=(server_socket,)).start()
    threading.Thread(target= outgoing_msg, args=(server_socket,)).start()

if __name__ == "__main__":
    main()