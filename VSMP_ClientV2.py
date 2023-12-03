import tkinter as tk 
import tkinter.ttk as ttk

from cryptography.fernet import Fernet  
import hashlib
import base64

import socket
from VSMP_ServerConnectTest2 import Sender
import time
from functools import lru_cache

from threading import Thread

class VSMPClient(tk.Tk):
    def __init__(self, username, keyWord, host, port):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))

            self.username=username
            self.keyWord=keyWord
            self.fkey=0
            self.HOST = host  # The server's hostname or IP address
            self.PORT = port  # The port used by the server
            self.recieve_open=True 
            self.recieved=[]
            self.snd=Sender() 
            
            self.recieve_thread = Thread(target=self.recieve_text)
            self.recieve_thread.daemon=True
            self.recieve_thread.start() 
            
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

        self.message.bind("<Return>", self.enter_pressed)
        
        self.greeting.grid(column=0, row=0, sticky=tk.N, pady=10)
        self.message_log.grid(column=0, row=1)
        self.message.grid(column=0, row=2,)
        self.send.grid(column=0, row=3, sticky=tk.S, pady=15)
        
        
        #print("it ran")
        
                #self.recieve_text()
                
    
    def text_insert(self, textBox, insertmessage, side="L"):
        if side=="R":
            self.message_log.tag_configure(side, justify="right")
        textBox.config(state=tk.NORMAL)
        textBox.insert(tk.END, insertmessage, side)
        textBox.yview(tk.END)
        textBox.config(state=tk.DISABLED)
    
    
    def getText(self):
        #self.recieve_open=False
        send_this=self.message.get("0.0", tk.END)
        self.message.delete("0.0", tk.END)
        self.send_text(self.encrypt(send_this))
        
    def enter_pressed(self, event):
        # Ignore the event object
        self.getText()
        self.message.delete("1.0", tk.END)
        
    def send_text(self, encMessage):
        self.printText(self.username, self.decrypt(encMessage), "R")
        self.snd.main(self.username, encMessage, self.HOST, self.PORT, 1)
        #self.recieve_open=True
        #self.recieve_text()  
        #print("enc: "+str(encMessage))
        #self.recieve_text()
                
    def recieve_text(self):
        #print("called")
        while self.recieve_open==True:
            time.sleep(.00001) 
            #print("...")      
            try:
                #print("test1")
                self.recieved=self.snd.recv_data  
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
            except:
                pass
            if self.recieved:
                #self.recieve_open=False
                self.handle_data()
                #self.recieve_open=True
        
        #print(self.recieved)
        #print(self.snd.recv_data)
        #self.printText(self.decrypt(encMessage))
    def handle_data(self):
        #print("test2")
        printed=False 
        while printed==False:
            try: 
                print("try")
                self.printText(str(self.recieved[0])[2:-1], self.decrypt(self.recieved[1]))
                print("good")
                printed=True
            except:
                printed=False
        #print("PRINTJNG TEXTTTTTT")
        self.recieved=[]
        self.snd.recv_data=[]
                    
    def printText(self, username, message, side="L"):
        #print("PRINTED???")
        line="-------------------------------"
        text=username+": "+ message
        if side=="R":
            self.text_insert(self.message_log, "\n"+line, "R")
            self.text_insert(self.message_log, "\n"+text, "R")
            self.text_insert(self.message_log, "\n"+line, "R")
        else:
            self.text_insert(self.message_log, "\n"+line)
            self.text_insert(self.message_log, "\n"+text)
            self.text_insert(self.message_log, "\n"+line)
        #print("dec: "+message)
    
    
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
            print(encMessage)
            raise ValueError("Invalid Fernet token length")
        fkey=self.gen_key(self.keyWord)
        message = fkey.decrypt(encMessage).decode()
        return message
    

if __name__ == "__main__":
    vsmp = VSMPClient("Vinny","Banana", "127.0.0.1", 42323)
    vsmp.recieve_open=True
    
    vsmp.mainloop()
    
    
    
    
    