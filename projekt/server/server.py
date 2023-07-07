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
sys_log = log_handler.sys_log
msg_buffer = []
connected_clients = []
lock = threading.Lock()
global_receiver = 'global'

#one incoming_msg thread for every client
def incoming_msg(client: Client):
        username, password = authenticate(client.socket, lock)

        #wait for authentication
        #  else msg's send by others clients during the authentication
        #  are send to this client after authentication (even when failed)
        with lock:
            #add socket to connected_clients for 'outgoing msg' thread
            connected_clients.append(client)

        #update username
        client.username = username
        #while client_socket is alive
        while not client.socket._closed:
            #recv msg from client of size DATASIZE
            msg = client.socket.recv(DATASIZE)
            commands_server.handle_commands(msg, client, connected_clients, msg_buffer, lock)
            #logs for system, global and private logs
            log_handler.handle_commands(username= client.username, data= msg)

#just one outgoing_msg thread
def outgoing_msg():
    while True:
        time.sleep(0.1)
        #if msg to send not empty and clients are available
        if msg_buffer != [] and connected_clients != []:
            
            #remove first msg from buffer
            with lock:        
                msg_to_send = msg_buffer.pop(0)
                msg_to_send : myMsg
                #format msg
                final_msg_to_send_bytes = msg_to_send.msg_header.format_msg(msg_to_send.client.username).get_header_msg_bytes()

            #send msg to client
            for client in connected_clients:
                client: Client
                #if client is still connected and client is not the sender of the msg
                if not client.socket._closed and client != msg_to_send.client:
                    #send msg to each client client
                    if msg_to_send.receiver_username == global_receiver:
                        client.socket.sendall(final_msg_to_send_bytes)
                    
                    #for pm msg
                    elif msg_to_send.receiver_username == client.username:
                        client.socket.sendall(final_msg_to_send_bytes)
                        break


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
        client = Client(socket=client_socket, adress=client_adress, username=None)

        sys_log.info(f'CLIENT:{client_adress}:connected')

        #new 'incoming msg' thread
        threading.Thread(target=incoming_msg, args=(client,)).start()



if __name__ == "__main__":
    main()