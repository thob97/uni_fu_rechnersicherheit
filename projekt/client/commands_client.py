import os
import sys
from header import Header

exit_chat = 'exit_chat'
show_history = 'show_history'
private_msg = 'pm'
send_file_command = 'send_file'
normal_msg = 'None'
DATASIZE = 1024

def print_available_commands():
    print(f'System: write "{exit_chat}" to exit')
    print(f'System: write "{private_msg}" to send a private message')
    print(f'System: write "{show_history}" to get a history chat history')
    print(f'System: write "{send_file_command}" to send a file')


#handle the client commands for outgoing msgs
def handle_msg_outgoing(msg, server_socket):
    if msg == exit_chat:
        os._exit(1)

    elif msg.find('\t') != -1:
        #dont allow as input \t as this is our seperator
        print('System: Please dont use tabs')

    elif msg == show_history:
        history_type = input('System: Write global or username for a private history: ')
        header = Header().create_header(show_history, history_type, None)
        server_socket.send(header.get_header_msg_bytes())

    elif msg == private_msg:
        receiver_username = input('System: Write his username: ')
        pm = input('System: Write your message: ')
        header = Header().create_header(private_msg, receiver_username, pm)
        server_socket.send(header.get_header_msg_bytes())

    elif msg == send_file_command:
        location = input('System: write the "file_location/filename:" ')
        #open file and send it
        with open(location, 'r') as file:
            data = file.read()
        header = Header().create_header(send_file_command, location, data)
        server_socket.send(header.get_header_msg_bytes())

    #send normal msg
    else:
        header = Header().create_header(normal_msg, None, msg)
        server_socket.send(header.get_header_msg_bytes())


#handle the client commands for incoming msgs
def handle_msg_incoming(data):
    command, option, msg = Header().return_header(data).get_information()

    if command == send_file_command:
        #TODO change msg later. 
        # option is the path
        if os.path.isfile(option):
            print(f'Another client tried to overwrite file {option}. File was not saved!')

        #open file and save data
        with open(option, 'w') as file:
            file.write(msg)
        print(f'System: Received file:{option}')

    #normal msg
    elif command == normal_msg or command == private_msg or command == show_history:
        print(msg)

    else:
        print(f'{command}, {option}, {msg}' )
        sys.exit('Msg Layout Error in:', data)