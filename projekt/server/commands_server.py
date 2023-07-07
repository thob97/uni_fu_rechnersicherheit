import sys
from classes import Client, myMsg, Header
import log_handler

show_history = 'show_history'
private_msg = 'pm'
send_file_command = 'send_file'
normal_msg = 'None'
global_receiver = 'global'
DATASIZE = 1024
sys_log = log_handler.sys_log

#remove client from connected_clients and exit the thread
def remove_client(client, connected_clients, lock):
    with lock:
        connected_clients.remove(client)
    sys_log.info(f'CLIENT:{client.adress}:disconnected')
    #stop thread
    sys.exit()

def handle_commands(data, client: Client, connected_clients, msg_buffer, lock):
        #if client disconnected from server
        if data == bytes(0):
            remove_client(client, connected_clients, lock)

        #else get the msg header information
        msg_header = Header().return_header(data)
        command, option, data = msg_header.get_information()

        if command == show_history:
            #ask log_handler for the correct log file
            log_data = log_handler.log_to_file(username_1= client.username, option= option)
            #create msg
            print(log_data)
            msg_header.msg = log_data.decode('utf-8')
            print(log_data.decode('utf-8'))
          
            msg = myMsg(msg_header= msg_header, client= Client(None,None,'Server'), receiver_username= client.username)
            #store msg in msg_buffer
            with lock:
                msg_buffer.append(msg)

        elif command == private_msg:
            #create msg
            msg = myMsg(msg_header= msg_header, client= client, receiver_username= option)
            #store msg in msg_buffer
            with lock:
                msg_buffer.append(msg)

        elif command == normal_msg or command == send_file_command:
            #create msg
            msg = myMsg(msg_header= msg_header, client= client, receiver_username= global_receiver)
            #store msg in msg_buffer
            with lock:
                msg_buffer.append(msg)

        else:
            sys.exit('Msg Layout Error in:', data)
