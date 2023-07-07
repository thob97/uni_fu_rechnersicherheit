private_msg = 'pm'
send_file_command = 'send_file'
#Defines the header of msg's
class Header():
    def __init__(self):
        self.seperator = '\t'
        self.command = ''
        self.option = ''
        self.msg = ''

    #gets the msg in a readable format for the server/client
    def get_header_msg_bytes(self):
        return bytes(f'{self.command}{self.seperator}{self.option}{self.seperator}{self.msg}', 'utf-8')

    def format_msg(self, sender_username):
        if self.command == private_msg:
            self.msg = f'{sender_username}_pm: {self.msg}'
        #dont format file
        elif self.command == send_file_command:
            pass
        else:
            self.msg = f'{sender_username}: {self.msg}' 
        return self

    def get_information(self):
        return self.command, self.option, self.msg

    #returns an already existing header from data
    def return_header(self, data):
        command, option, msg = data.decode('utf-8').split(self.seperator, 2)
        self.command = command
        self.option = option
        self.msg = msg
        return self

    def create_header(self, command, option, msg):
        self.command = command
        self.option = option
        self.msg = msg
        return self

class Client():
    def __init__(self,socket,adress,username):
        self.socket = socket
        self.adress = adress
        self.username = username 

class myMsg():
    def __init__(self,msg_header: Header,client: Client,receiver_username):
        self.msg_header = msg_header
        self.client = client
        self.receiver_username = receiver_username