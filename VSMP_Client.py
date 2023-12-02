import tkinter as tk 
import tkinter.ttk as ttk

from cryptography.fernet import Fernet  
import hashlib
import base64

import socket

class VSMPClient(tk.Tk):
    def __init__(self, username, keyWord):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))

            self.username=username
            self.keyWord=keyWord
            self.fkey=0

            ww = 600
            wh = 625
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = int(sw / 2 - ww / 2)
            cy = int(sh / 2 - wh / 2)
            self.geometry(f"{ww}x{wh}+{cx}+{cy}")
            self.minsize(width=300, height=625)
            self.message_Frame()
    
   
    def message_Frame(self):
        self.messageFrame=tk.Frame(master=self, bg="pink", padx=25, pady=25)
        self.messageFrame.columnconfigure([0,1], weight=1)
        self.messageFrame.rowconfigure([0,3], weight=1)

        self.greeting = tk.Label(master=self.messageFrame, text="YOU ARE CHATTING WITH:")
        self.message= tk.Text(master=self.messageFrame, height=5)
        self.message_log= tk.Text( master=self.messageFrame, height=15, yscrollcommand=True)
        self.send=tk.Button(master=self.messageFrame, text="SEND", padx=50, pady=25, bg="blue", command=lambda:self.getText())  

        self.text_insert(self.message_log, "THIS IS A MESSAGE AHHH OMG YOU GOT MAILLLLLL")

        self.messageFrame.pack(padx=25, pady=25, fill=tk.BOTH)

        self.greeting.grid(column=0, row=0, sticky=tk.N, pady=10)
        self.message_log.grid(column=0, row=1)
        self.message.grid(column=0, row=2,)
        self.send.grid(column=0, row=3, sticky=tk.S, pady=15)

    def text_insert(self, textBox, insertmessage, side="L"):
        if side=="R":
            self.message_log.tag_configure(side, justify="right")
        textBox.config(state=tk.NORMAL)
        textBox.insert(tk.END,insertmessage, side)
        textBox.config(state=tk.DISABLED)

    def getText(self):
        send_this=self.message.get("1.0", tk.END)
        self.message.delete("1.0", tk.END)
        self.send_text(self.encrypt(send_this))
    
    def send_text(self, encMessage):
        #Sending code here
        self.printText(self.decrypt(encMessage), "R")
        print("enc: "+str(encMessage))
        self.recieve_text(encMessage)
        
        #NEW SERVER CODE MAY NEED FIX
        self.HOST = "127.0.0.1"  # The server's hostname or IP address
        self.PORT = 65432  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

        print(f"Received {data!r}")
        
    def recieve_text(self, encMessage):
        #recieveing code here
        self.printText(self.decrypt(encMessage))
        
    
    def printText(self, message, side="L"):
        line="--------------------------------"
        text=self.username+": "+ message
        if side=="R":
            self.text_insert(self.message_log, "\n"+line, "R")
            self.text_insert(self.message_log, "\n"+text, "R")
            self.text_insert(self.message_log, "\n"+line, "R")
        else:
            self.text_insert(self.message_log, "\n"+line)
            self.text_insert(self.message_log, "\n"+text)
            self.text_insert(self.message_log, "\n"+line)
        print("dec: "+message)
    
    def gen_key(self, keyword):
        if not self.fkey:
            keyword_bytes = keyword.encode('utf-8')
            key_bytes = hashlib.sha256(keyword_bytes).digest()[:32]
            key = base64.urlsafe_b64encode(key_bytes)
            self.fkey = Fernet(key)
        return self.fkey
    
    def encrypt(self, message):
        fkey=self.gen_key(self.keyWord)
        encMessage = fkey.encrypt(message.encode())
        #print(self.fkey.decrypt(encMessage).decode())
        return encMessage
    
    def decrypt(self, encMessage):
            # Check if encMessage is a valid Fernet token
        if not isinstance(encMessage, bytes):
            raise TypeError("encMessage must be of type bytes")

        # Check if encMessage has the correct structure
        if len(encMessage) < 32:
            raise ValueError("Invalid Fernet token length")
        fkey=self.gen_key(self.keyWord)
        message = fkey.decrypt(encMessage).decode()
        return message
    

if __name__ == "__main__":
    vsmp = VSMPClient("Vinny","Banana")
    vsmp.mainloop()