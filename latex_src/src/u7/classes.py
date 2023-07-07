class Client():
    def __init__(self,socket,adress,username):
        self.socket = socket
        self.adress = adress
        self.username = username 

class myMsg():
    def __init__(self,msg,client: Client):
        self.msg = msg
        self.client = client

    def format_msg(self):
        b_msg = self.msg.decode('utf-8')
        return bytes(f'{str(self.client.username)}: {b_msg}', 'utf-8')

    def format_pm(self):
        return bytes(f'{str(self.client.username)}_pm: {self.msg}', 'utf-8')