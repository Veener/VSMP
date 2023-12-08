
#python VSMP_ServerV2 127.0.0.1 42323
import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
clientList=[]

class ClientConnection():
    def accept_wrapper(self, sock):
        self.conn, self.addr = sock.accept()  # Should be ready to read
        clientList.append(sock)
        for client in clientList:
            print(client)
        print(f"Accepted connection from {self.addr}")
        self.conn.setblocking(False)
        self.data = types.SimpleNamespace(addr=self.addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(self.conn, events, data=self.data)

    def service_connection(self, key, mask):
        self.sock = key.fileobj
        self.data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = self.sock.recv(4096)  # Should be ready to read
            print(recv_data)
            print(":::TEST1:::")
            if recv_data:
                messages = recv_data.split(b"\0")  # Assuming the delimiter is a null byte
                print(messages)
                print(":::TEST2:::")
                # Send each message individually
                for message in messages:
                    for sock in clientList:
                        if message:
                            sock.send(message)
                            print(f"Echoing {message!r} to {self.data.addr}")
                
                # Reset recv_data to an empty byte string
                recv_data = b""
            else:
                recv_data = b""
                print(f"Closing connection to {self.data.addr}")
                sel.unregister(self.sock)
                self.sock.close()

    def main(self):
        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()
            
host="127.0.0.1"
port=42323
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
    
if __name__=="__main__":
     x=ClientConnection() 
     x.main()             
