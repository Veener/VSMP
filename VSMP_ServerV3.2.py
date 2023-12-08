#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket
import time


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
        serverRescue()
    except Exception as e:
        print(f"Handler Error: {e}")
    finally:
        conn.close()
        clientList.remove(conn)
        print(f"Connection to client ({addr[0]}: {addr[1]}) closed")

def broadcast(messages,  username):
    if not messages or not clientList:
        print("NAHT")
        return
    """print(str(username)[2:-1])
    usernameCol=str(username)[2:-1] + ": "
    usernameCol
    messages.pop(0)"""
    print(f"Messages: {messages}")
    messageList=b""
    for message in messages:
        if not message:
            print("empty byte. Breaking")
            break
        messageList+=message
        messageList += b"\0"
        print(f"#{username}: {message}")
    print("created ML")
    try:
        for client in clientList:    
            client.send(bytes(messageList))
            time.sleep(.001)
            print(f"sent to {client}")
        print(f"ML={username}: {messageList}")
    except KeyboardInterrupt:
        print("Manual Break")
        serverRescue()
    finally:
        print("done sending")
        
def serverRescue():
    for client in clientList: 
        client.close()
        clientList.remove(client)
    print(f"Server Rescued. All connections severed")
    
        
    """for client in clientList:
        print("t1")
        #print(f"Client: {client}")
        try:
            print("t2")
            for message in messages:
                print(f"p1{username}: {message}")
                print("t3")
                client.send(bytes(usernameCol.encode("utf-8"))+bytes(message))
                time.sleep(.001)
                
        finally:
            print("done sending")"""
    

def __init__():
    host="127.0.0.1"
    #host="192.168.4.97"
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
    except KeyboardInterrupt:
        print("Manual Break")
        serverRescue()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()
        print("Server closed")

if __name__=="__main__":
    __init__()

   
    
