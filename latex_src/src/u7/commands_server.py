import sys
from classes import Client, myMsg
import log_handler

log = log_handler.log
show_history = 'show_history'
private_msg = 'pm'
DATASIZE = 1024

#remove client from connected_clients and exit the thread
def remove_client(client, connected_clients, lock):
    with lock:
        connected_clients.remove(client)
        log.info(f'{client.adress}: disconnected')
    #stop thread
    sys.exit()

def send_pm(sender: Client, connected_clients):
    sender.socket.sendall(b'System: Write his username:')
    username = sender.socket.recv(DATASIZE).decode('utf-8')
    sender.socket.sendall(b'System: Write your message:')
    pm = sender.socket.recv(DATASIZE).decode('utf-8')
    
    #search for the receiver
    for receiver in connected_clients:
        receiver: Client
        #if the user is online, send him the msg
        if receiver.username == username:
            #send the msg
            receiver.socket.sendall(myMsg(pm, sender).format_pm())
            #log
            log_msg = f'{sender.username} wrote: {pm} to {receiver.username} as pm'
            log.info(log_msg)
            log_handler.pm_user_log(log_msg, sender.username, receiver.username)
            break

def send_history(client: Client):
    client.socket.sendall(b'System: Write global or username for a private history:')
    global_or_username = client.socket.recv(DATASIZE).decode('utf-8')

    if global_or_username == 'global':
        data = log_handler.log_to_file('log', None)
        client.socket.sendall(data)
    else:
        data = log_handler.log_to_file(client.username, global_or_username)
        client.socket.sendall(data)


def handle_commands(data, client: Client, connected_clients, msg_buffer, lock):
    msg = data.decode('utf-8')

    #if client disconnected from server
    if data == bytes(0):
        remove_client(client, connected_clients, lock)

    elif msg == show_history:
        send_history(client)

    elif msg == private_msg:
        send_pm(client, connected_clients)
    
    #normal msg
    else:
        #store msg in msg_buffer
        with lock:
            msg_buffer.append(myMsg(data, client))

