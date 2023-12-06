#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket


usernameList=[]
clientList=[]


def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            dataL = data.split(b"\0")
            username=dataL[0]
            dataL.pop()
            
            """data2=data.decode("utf-8")
            if data2.lower() == "close":
                conn.send("closed".encode("utf-8"))
                break
            print(f"Received: {data2}")
            # convert and send accept response to the client
    
            #conn.send(data)"""
            broadcast(dataL, username)
    except KeyboardInterrupt:
        print("KeyStop")
        pass
    except Exception as e:
        print(f"Handler Error: {e}")
    finally:
        conn.close()
        clientList.remove(conn)
        print(f"Connection to client ({addr[0]}: {addr[1]}) closed")

def broadcast(messages,  username):
    print(str(username)[2:-1])
    usernameCol=str(username)[2:-1] + ": "
    usernameCol
    messages.pop(0)
    print(f"Messages: {messages}")
    for client in clientList:
        print("t1")
        #print(f"Client: {client}")
        try:
            print("t2")
            for message in messages:
                print(f"p1{username}: {message}")
                print("t3")
                client.send(bytes(usernameCol.encode("utf-8"))+bytes(message))
                
        finally:
            print("done sending")
    

def __init__():
    host="127.0.0.1"
    port=42323
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        print(f"Listening on {host}: {port}")
        
        
        while True:
            conn, addr=s.accept()
            clientList.append(conn)
            
            print(f"got clinet from{addr[0]}: {addr[1]}")
            thread=threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()
        print("Server closed")

if __name__=="__main__":
    __init__()

   
    
