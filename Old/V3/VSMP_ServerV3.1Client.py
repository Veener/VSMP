#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket



def __init__():
    host="127.0.0.1"
    port=42323
    global c
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))
    listenThread=threading.Thread(target=listen)
    sendThread=threading.Thread(target=sendData)
    print("listening")
    listenThread.start()
    print("sending")   
    sendThread.start()
    
    
def listen():
    while True: 
        try:       
            response=c.recv(4096)
            print(f"response: {response}")
            response=response.decode("utf-8")
            print(response[0])
            if response[0]=="!":
                print("USER TAKEN LOL")
            else:
                print(f"{response}")
        except Exception as e:
            print(f"ClientSide error: {e}")  
            c.close()
            print("client closed")
            break
 
def sendData():
    while True:
        data=""
        data = input()
        dataL2=data.split("|")
        print(dataL2)
        dataL=[]
        for x in dataL2:
            dataL.append(x.encode("utf-8"))
        print(dataL)
        send_this=b""
        for x in dataL:
            send_this += x
            send_this += b"\0"
        print(send_this)
        c.send(send_this)


if __name__=="__main__":
    __init__()

   
    
