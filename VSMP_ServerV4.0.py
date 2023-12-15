#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket
import time
import datetime


usernameList={
    "username": "",
    "close": "",
    "SERVER": ""
}
clientList=[]


def __init__():
    host="127.0.0.1"    #Local Host
    #host="192.168.4.97" #Home
    #host ="10.255.34.38" #School
    port=42323
    
    inpthread=threading.Thread(target=serverInput)
    inpthread.start()
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()
        logprint(f"Listening on {host}: {port}")
        
        while True:
            conn, addr=s.accept()
            clientList.append(conn)
            
            logprint(f"Client from {addr[0]}: {addr[1]} has connected")
            thread=threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        logprint("Manual Break")
        serverRescue()
    except Exception as e:
        logprint(f"Error: {e}")
    finally:
        s.close()
        logprint("Server closed")


def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(4096)
            if data:
                dataL = data.split(b"\0")
                #print(f"Data:{data}, dataL:{dataL}")
                username=str(dataL[0].decode("utf-8"))
                #print(username)
                #print(f"USernma fr:{dataL[2]}")
                #print(f"Data: {dataL}")
                dataL.pop()
                if username=="SERVER":
                    serverMessageHandler(dataL, conn)
                else:    
                    #print("Bcast")
                    broadcast(dataL, username)
            else:
                pass

            
    except KeyboardInterrupt:
        logprint("KeyStop")
        serverRescue()
    except Exception as e:
        logprint(f"Handler Error: {e}")
    finally:
        closeClient(conn)
        logprint(f"Connection to client ({addr[0]}: {addr[1]}) closed\n")

def broadcast(messages,  username):
    if not messages or not clientList:
        logprint("NAHT")
        return
    """print(str(username)[2:-1])
    usernameCol=str(username)[2:-1] + ": "
    usernameCol
    messages.pop(0)"""
    logprint(f"Message: {messages}")
    messageList=b""
    for message in messages:
        if not message:
            logprint("empty byte. Breaking")
            break
        messageList+=message
        messageList += b"\0"
        #print(f"#{username}: {message}")
    #print("created ML")
    try:
        x=0
        for client in clientList: 
            x+=1   
            client.send(bytes(messageList))
            time.sleep(.001)
            #print(f"sent to {client}")
        #print(f"ML={username}: {messageList}")
        #logprint(f"Message sent to {x}/{len(usernameList)-3} users\n")
    except KeyboardInterrupt:
        logprint("Manual Break")
        serverRescue()
    finally:
       logprint(f"Message sent to {x}/{len(usernameList)-3} users\n")
 
def serverInput():
    while True:
        inp=input().lower()
        if inp=="serverr":
            serverRescue()
        elif inp=="kick":
            uname=input("Kick Who?")
            kickClient(uname)
        elif inp=="sb":
            message=input("Message: ")
            serverBroadcast(message)
        elif inp=="ul":
            logprint(usernameList.keys())
        else:
            logprint("invalid command")
            
def serverBroadcast(message):
    try:
        for client in clientList:    
            client.send(bytes(f"#SERVER: {message}".encode("utf-8")))
            logprint(f"SB to {client}")
    except KeyboardInterrupt:
        logprint("Manual Break")
        serverRescue()
    finally:
        logprint("done SB\n")
        
def serverRescue():
    x=0
    for client in clientList: 
        closeClient(client)
        x=+1
    logprint(f"Server Rescued. All({x}) connections severed\n")
    
def closeClient(client):
    logprint(f"client at {client} Will be closed")
    client.close()
    if client in clientList:
        clientList.remove(client)
    for key, value in usernameList.items():
        if value == client:
            del usernameList[key]
            logprint(f"{key} has left the chat")
            break
    
  
def kickClient(username):
    conn=usernameList[username]
    conn.send("*You have been kicked!".encode("utf-8"))
    logprint(f"!{username} has been kicked!")   
    closeClient(conn) 
  
   
def checkUsername(username, conn):
    if username in usernameList.keys():
        conn.send("*Username Taken, Try a New One!".encode("utf-8"))
        logprint(bytes("!Username Taken, Try a New One!".encode("utf-8")))
        logprint(usernameList.keys())
        closeClient(conn)
    else:
        usernameList[username]=conn
        logprint(f"Adding username: {username}\n")
        #print(usernameList)

def keyWarn(username):
    client=usernameList[username]
    client.send(b"!A conencted user has a non-compatable key and did not recieve your message!")
    logprint(f"Key Warned {username}")

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
        logprint("Server Message Not Handled")
        
def logprint(message):
    now = datetime.datetime.now()
    t=now.strftime("%H:%M:%S")
    cdate=datetime.date.today()
    
    fdate = cdate.strftime("%m-%d-%Y")

    print(f"{t} | {message}")
    with open(f'ServerLogs/{fdate}.txt', 'a') as file:
        file.write(f"{t} | {message}\n")
    
if __name__=="__main__":
    __init__()

   
    
