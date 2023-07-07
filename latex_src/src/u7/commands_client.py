import os

exit_chat = 'exit_chat'
show_history = 'show_history'
private_msg = 'pm'
send_file_command = 'send_file'
DATASIZE = 1024

def print_available_commands():
    print(f'System: write "{exit_chat}" to exit')
    print(f'System: write "{private_msg}" to send a private message')
    print(f'System: write "{show_history}" to get a history chat history')
    print(f'System: write "{send_file_command}" to send a file')

def send_file(server_socket):
    location = input('System: write the "file_location/filename:" ')
    #open file and send it
    with open(location, 'rb') as file:
        server_socket.send(file.read())

#handle the client commands
def handle_commands(msg, server_socket):

    if msg == exit_chat:
        os._exit(1)
    
    if msg == send_file_command:
        send_file(server_socket)

    #send normal msg
    else:
        server_socket.send(bytes(msg, 'utf-8'))

