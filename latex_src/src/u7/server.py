import socket
import threading
import time
from authentication_server import authenticate
from classes import Client, myMsg
import commands_server
import log_handler

IP = "0.0.0.0"
PORT = 1234
DATASIZE = 1024
msg_buffer = []
connected_clients = []
lock = threading.Lock()
log = log_handler.log

#one incoming_msg thread for every client
def incoming_msg(client: Client):
        username, password = authenticate(client.socket, lock)
        #update username
        client.username = username
        #while client_socket is alive
        while not client.socket._closed:
            #recv msg from client fo size DATASIZE
            msg = client.socket.recv(DATASIZE)
            commands_server.handle_commands(msg, client, connected_clients, msg_buffer, lock)

#just one outgoing_msg thread
def outgoing_msg():
    while True:
        time.sleep(1)
        #if msg to send not empty and clients are available
        if msg_buffer != [] and connected_clients != []:
            #send msg to each client
            for client in connected_clients:
                client: Client
                #if client is still connected and client is not the sender of the msg
                if not client.socket._closed and client != msg_buffer[0].client:
                    #send msg to client
                    client.socket.sendall(msg_buffer[0].format_msg())
            #remove msg from bugger
            with lock:        
                log_msg = msg_buffer.pop(0)
                #write msg to log
                log_msg = log_msg.format_msg().decode('utf-8')
                log.info(f'msg send: {log_msg}')


def main():
    #create socket(IP4, tcp)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP,PORT))
    #listen for connections
    server_socket.listen()

    #new 'outgoing msg' thread
    threading.Thread(target=outgoing_msg).start()

    while True:
        #new connecting client
        client_socket, client_adress = server_socket.accept()
        client = Client(client_socket, client_adress, None)

        log.info(f'new connection from: {client_adress}')

        #new 'incoming msg' thread
        threading.Thread(target=incoming_msg, args=(client,)).start()

        #add socket to connected_clients for 'outgoing msg' thread
        with lock:
            connected_clients.append(client)

if __name__ == "__main__":
    main()