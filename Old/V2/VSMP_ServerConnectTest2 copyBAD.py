# multiconn-client.py


#python VSMP_ServerConnectTest2.py 127.0.0.1 42323 2
import sys
import socket
import selectors
import types


class Sender():
    def main(self, message, host, port, num_conns):
            self.sel = selectors.DefaultSelector()
            self.messages=message
            #self.messages = bytes(message, encoding="utf-8")
            
            """if len(sys.argv) != 4:
                print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
                sys.exit(1)

            host, port, num_conns = sys.argv[1:4]"""
            self.start_connections(host, int(port), int(num_conns))

            try:
                while True:
                    events = self.sel.select(timeout=1)
                    if events:
                        for key, mask in events:
                            self.service_connection(key, mask)
                    # Check for a socket being monitored to continue.
                    if not self.sel.get_map():
                        break
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
            finally:
                self.sel.close()


    def start_connections(self, host, port, num_conns):
        messages=self.messages
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
                msg_total=sum(len(m) for m in messages),
                recv_total=0,
                messages=self.messages,
                outb=b"",
            )
            self.sel.register(sock, events, data=data)


    def service_connection(self, key, mask):
        messages=self.messages
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print(f"Received {recv_data!r} from connection {data.connid}")
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print(f"Closing connection {data.connid}")
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            #data.outb=data.messages
            if not data.outb and data.messages:
                data.outb = data.messages
            if data.outb:
                print(f"Sending {data.outb!r} to connection {data.connid}")
                sent = sock.send(bytes(data.outb, encoding="utf-8")  # Should be ready to write
                data.outb = data.outb[sent:]

    