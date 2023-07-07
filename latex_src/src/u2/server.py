import socket
import threading
import time
import sys
from datetime import datetime

IP = "127.0.0.1"
PORT = 1234
DATASIZE = 1024
msg_buffer = []
connected_clients = []
lock = threading.Lock()

class myMsg():
    def __init__(self,msg,socket,adress):
        self.msg = msg
        self.socket = socket
        self.adress = adress

    def get_final_msg_bytes(self):
        return bytes((str(self.adress) +': '+ self.msg.decode('utf-8')), 'utf-8')

class myThread(threading.Thread):
    def __init__(self, tid, client_socket, client_adress):
        threading.Thread.__init__(self)
        self.tid = tid
        self.client_socket = client_socket
        self.client_adress = client_adress

    def run(self):
        #incoming msg thread
        if self.tid == 0:
            #while client_socket is alive
            while not self.client_socket._closed:
                #recv msg from client fo size DATASIZE
                msg = self.client_socket.recv(DATASIZE)
                #if client disconnected
                if msg == bytes(0):
                    #remove client from connected_clients and exit
                    with lock:
                        connected_clients.remove(self.client_socket)
                        #write disconnect to log
                        with open('log.txt', 'a') as file:
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            file.write(date + ': ' + str(self.client_adress) + ' disconnected\n')
                    #stop thread
                    sys.exit()
                #store msg in msg_buffer
                with lock:
                    msg_buffer.append(myMsg(msg, self.client_socket, self.client_adress))

        #outgoing msg thread
        if self.tid == 1:
            while True:
                time.sleep(1)
                #if msg to send not empty and clients are available
                if msg_buffer != [] and connected_clients != []:
                    #send msg to each client
                    for s in connected_clients:
                        #if client is still connected and client is not the sender of the msg
                        if not s._closed and s != msg_buffer[0].socket:
                            #send msg to client
                            s.sendall(msg_buffer[0].get_final_msg_bytes())
                    #remove msg from bugger
                    with lock:        
                        mymsg = msg_buffer.pop(0)
                        #write msg to log
                        with open('log.txt', 'a') as file:
                            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            file.write(date + ': ' + 'msg send: "' + mymsg.get_final_msg_bytes().decode('utf-8') + '" \n')



if __name__ == "__main__":
    #create socket(IP4, tcp)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP,PORT))
    #listen for connections
    server_socket.listen()

    #new 'outgoing msg' thread
    myThread(1,None, None).start()

    while True:

        #new connecting client
        client_socket, client_adress = server_socket.accept()

        #write in log
        with open('log.txt', 'a') as file:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            file.write(date +': new connection from' + str(client_adress) +'\n') 

        #new 'incoming msg' thread
        myThread(0,client_socket, client_adress).start()

        #add socket to connected_clients for 'outgoing msg' thread
        with lock:
            connected_clients.append(client_socket)