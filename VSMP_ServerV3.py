#python VSMP_ServerV2 127.0.0.1 42323
import sys
import socket
import selectors
import types

usernameList=[]
clientList=[]
def __init__():
    host="127.0.0.1"
    port=42323
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"Listening on {host}:{port}")
    s.setblocking(False)

def handle():
    #Always listnening
    #might be esier to clinet hdle due to encryption
    print("handle")
def broadcast(messages):
    #Run when gor message
    for client in clientList:
        #if client != sock:
        for message in messages:
            client.send(message)
            print(f"Echoing {message!r} to {client.getpeername()}")
def recieve(conn, addr):
    while True:
        data = conn.recv(4096)
        if data:
            broadcast(data)
            break
    #Always listening
    #then run broadcast
def newConnection():
   conn, addr=s.accept()
   recieve(conn, addr)
    
