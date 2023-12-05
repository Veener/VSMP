#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket


usernameList=[]
clientList=[]
MessageQueue=[]

def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            MessageQueue.append(data)
            data2=data.decode("utf-8")
            
            if data2.lower() == "close":
                conn.send("closed".encode("utf-8"))
                break
            print(f"Received: {data2}")
            # convert and send accept response to the client
    
            conn.send(data)
            
            broadcast()
    except KeyboardInterrupt:
        print("KeyStop")
        pass
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        conn.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def broadcast():
    for client in clientList:
        for message in MessageQueue:
            client.send(message)
            print(message)
    MessageQueue=[]
    

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

   
    
