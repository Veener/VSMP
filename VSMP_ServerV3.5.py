#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket
import time


usernameList={
    "username": ""
}
clientList=[]


def __init__():
    host="127.0.0.1"    #Local Host
    #host="192.168.4.97" #Home
    #host ="10.255.34.38" #School
    port=42323
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        print(f"Listening on {host}: {port}")
        
        while True:
            conn, addr=s.accept()
            clientList.append(conn)
            
            print(f"got client from{addr[0]}: {addr[1]}")
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


def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            if data:
                dataL = data.split(b"\0")
                print(f"Data:{data}, dataL:{dataL}")
                username=str(dataL[0].decode("utf-8"))
                #print(username)
                #print(f"USernma fr:{dataL[2]}")
                dataL.pop()
                if username=="SERVER":
                    serverMessageHandler(dataL, conn)
                else:    
                    print("Bcast")
                    broadcast(dataL, username)
            else:
                pass

            
    except KeyboardInterrupt:
        print("KeyStop")
        serverRescue()
    except Exception as e:
        print(f"Handler Error: {e}")
    finally:
        closeClient(conn)
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
    x=0
    for client in clientList: 
        closeClient(client)
        x=+1
    print(f"Server Rescued. All({x}) connections severed")
    
def closeClient(client):
    print(f"client at {client} Will be closed")
    client.close()
    if client in clientList:
        clientList.remove(client)
    for key, value in usernameList.items():
        if value == client:
            del usernameList[key]
            print(f"removed {key} from usernameList")
            break
    
  
def kickClient(username):
    conn=usernameList[username]
    conn.send("!You have been kicked!".encode("utf-8"))
    print("!Username Taken, Try a New One!")   
    closeClient(conn) 
  
   
def checkUsername(username, conn):
    if username in usernameList.keys():
        conn.send("!Username Taken, Try a New One!".encode("utf-8"))
        print(bytes("!Username Taken, Try a New One!".encode("utf-8")))
        print(usernameList.keys())
        closeClient(conn)
    else:
        usernameList[username]=conn
        print(f"Adding username :{username}")
        print(usernameList)

def keyWarn(username):
    client=usernameList[username]
    client.send(b"!A conencted user has a non-compatable key and did not recieve your message!")
    print(f"Key Warned {username}")

def serverMessageHandler(dataL, conn):
    type=dataL[1].decode("utf-8")
    message=dataL[2].decode("utf-8")
    if type=="username":
        checkUsername(message, conn)
    elif type=="close":
        closeClient(usernameList[message])
    elif type=="kick":
        kickClient(message)
    elif type=="KeyWarn":
        keyWarn(message)
    else:
        print("Server Message Not Handled")

if __name__=="__main__":
    __init__()

   
    
