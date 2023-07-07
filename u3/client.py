import socket
import threading
import os
import time

IP = "0.0.0.0"
PORT = 1234
DATASIZE = 1024

class myThread(threading.Thread):
    def __init__(self, tid, server_socket):
        threading.Thread.__init__(self)
        self.tid = tid
        self.server_socket = server_socket


    def run(self):
        #incoming msg thread
        if self.tid == 0:
            #while server_socket is alive
            while not self.server_socket._closed:
                #waits for msg from server of size DATASIZE
                msg = self.server_socket.recv(DATASIZE)
                #print msg
                print(msg.decode('utf-8'))

        #outgoing msg thread
        if self.tid == 1:
            #while server_socket is alive
            while not self.server_socket._closed:
                #wait for keyboard input
                msg = input()
                if msg == 'exit':
                    os._exit(1)
                #send msg
                server_socket.send(bytes(msg, 'utf-8'))


if __name__ == "__main__":
    #connect socket(IP4, tcp)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((IP,PORT))

    #incoming msg thread
    myThread(0,server_socket).start()

    #outgoing msg thread
    myThread(1,server_socket).start()

