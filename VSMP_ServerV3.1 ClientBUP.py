#python VSMP_ServerV2 127.0.0.1 42323
import threading
import socket



def __init__():
    host="127.0.0.1"
    port=42323
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))
    try: 
        while True:
            data = input("Data:")
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
            
            response=c.recv(4096)
            response=response.decode("utf-8")
            
            if response.lower() == "closed":
                break

            print(f"Received: {response}")
    except Exception as e:
        print(f"ClientSide error: {e}")
    finally:   
        c.close()
        print("client closed")
 

if __name__=="__main__":
    __init__()

   
    
