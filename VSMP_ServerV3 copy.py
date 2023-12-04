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
    print(f"Listening on {host}: {port}")
    
    conn, addr=s.accept()
    print(f"got clinet from{addr[0]}: {addr[1]}")
    while True:
        data = conn.recv(4096)
        data=data.decode("utf-8")
        
        if data=="close":
            conn.send("closed".encode("utf-8"))
            break
        print(f"Received: {data}")
        
        response=data.encode("utf-8")
        conn.send(response)
    conn.close()
    print("Server closed")
    s.close()

if __name__=="__main__":
    __init__()

   
    
