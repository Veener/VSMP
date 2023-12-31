# multiconn-client.py


#python VSMP_ServerConnectTest2.py 127.0.0.1 42323 2
import sys
import socket
import selectors
import types
import time
from threading import Thread

class Sender():
    def main(self, user, message, host, port, num_conns):
        self.sel = selectors.DefaultSelector()
        if type(user)!=bytes:
            user=user.encode("utf-8")
        if type(message)!=bytes:
            message=message.encode("utf-8")
        self.messages = [user, message]
        self.recv_data=[]
        
        self.start_connections(host, int(port), int(num_conns))
        while True:
            try:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:           
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
            #self.sel.close()


    def start_connections(self, host, port, num_conns):
        server_addr = (host, port)
        for i in range(0, num_conns):
            connid = i + 1
            print(f"Starting connection {connid} to {server_addr}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in self.messages),
                recv_total=0,
                messages=self.messages.copy(),
                outb=b"",
            )
            self.sel.register(sock, events, data=data)


    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        while True: 
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(4096)  # Should be ready to read
                if recv_data:
                    print(f"Received {recv_data!r} from connection {data.connid}")
                    self.recv_data.append(recv_data)
                    data.recv_total += len(recv_data)
                if data.recv_total == data.msg_total:
                    print(f"Closing connection {data.connid}")
                    #self.sel.unregister(sock)
                    #sock.close()
                    recv_data=[]
                if not recv_data:
                    print("waiting")
            if mask & selectors.EVENT_WRITE:
                if not data.outb and data.messages:
                    data.outb = data.messages.pop(0)
                    data.outb += b"\0"  # Add delimiter to the end of each message
                if data.outb:
                    print(f"Sending {data.outb!r} to connection {data.connid}")
                    #time.sleep(0.1)  Used to be needed, but delimiter does same but better
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]




        