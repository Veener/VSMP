import tkinter as tk 
import tkinter.ttk as ttk

from cryptography.fernet import Fernet  
import hashlib
import base64

import socket
import time

from threading import Thread

class VSMPClient(tk.Tk):
    def __init__(self, username, keyWord, host, port):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))

            self.fkey=0
            self.recieve_open=True 
            self.received=""
            
            
            #self.recieve_thread.daemon=True

            
            ww = 600
            wh = 625
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = int(sw / 2 - ww / 2)
            cy = int(sh / 2 - wh / 2)
            self.geometry(f"{ww}x{wh}+{cx}+{cy}")
            self.minsize(width=300, height=625)
            self.loginWindow()
            
    #login Window Running+Handling
     
    def loginWindow(self):
        self.win2=tk.Toplevel()
        self.win2.title("VSMP Login")
        #self.iconbitmap("D:/SpaceShuttle.ico")
        self.win2.attributes("-topmost", 1)
        self.win2.style=ttk.Style(self)
        self.win2.style.configure("TButton", font=("Helvetica", 24))



        ww = 300
        wh = 200
        sw = self.win2.winfo_screenwidth()
        sh = self.win2.winfo_screenheight()
        cx = int(sw / 2 - ww / 2)
        cy = int(sh / 2 - wh / 2)
        self.win2.geometry(f"{ww}x{wh}+{cx}+{cy}")
        self.win2.minsize(width=300, height=150)
        self.win2.lift(self)
        self.login_frame()
    
    def login_frame(self):
        self.loginFrame=tk.Frame(master=self.win2, bg="pink", padx=25, pady=25)

        self.username_text=tk.Label(master=self.loginFrame, text="Username:", bg="pink",)
        self.username_input=tk.Entry(master=self.loginFrame,)
        self.key_text=tk.Label(master=self.loginFrame, text="Key:", bg="pink",)
        self.key_input=tk.Entry(master=self.loginFrame,)
        self.host_text=tk.Label(master=self.loginFrame, text="Host:", bg="pink",)
        self.host_input=tk.Entry(master=self.loginFrame,)
        self.host_input.insert(1,"127.0.0.1")
        self.port_text=tk.Label(master=self.loginFrame, text="Port:", bg="pink",)
        self.port_input=tk.Entry(master=self.loginFrame,)
        self.port_input.insert(1,"42323")

        self.login_button=tk.Button(master=self.loginFrame, text="Login", command=lambda: self.login())

        self.loginFrame.pack(padx=25, pady=25, fill=tk.BOTH)

        self.username_text.grid(row=0, column=0,)
        self.username_input.grid(row=0, column=1, columnspan=2)
        self.key_text.grid(row=1, column=0)
        self.key_input.grid(row=1, column=1, columnspan=2)
        self.host_text.grid(row=2, column=0,)
        self.host_input.grid(row=2, column=1, columnspan=2)
        self.port_text.grid(row=3, column=0)
        self.port_input.grid(row=3, column=1, columnspan=2)
        self.login_button.grid(row=4, column=1, columnspan=2)
        
    def login(self):
        self.username=self.username_input.get()
        self.keyWord=self.key_input.get()
        self.host=self.host_input.get()
        self.port=int(self.port_input.get())
        
        self.message_Frame()
        self.serverConnect()  
        self.win2.destroy()
          
    #Main Window Running+Server Connect

    def message_Frame(self):
        self.messageFrame=tk.Frame(master=self, bg="pink", padx=25, pady=25)
        self.messageFrame.columnconfigure([0,1], weight=1)
        self.messageFrame.rowconfigure([0,3], weight=1)

        self.greeting = tk.Label(master=self.messageFrame, text=f"YOU ARE CHATTING WITH:{self.username}")
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
                
    def serverConnect(self):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((self.host, self.port))
        self.listenThread=Thread(target=self.listen)
        #print("listening")
        self.listenThread.start()
        #print("sending") 
        print(f"Connected to Server at {self.host}: {self.port}")
        self.sendData("username", bytes(self.username.encode("utf-8")))
 
    #Text Managment
    
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
        return "break"
        
    def send_text(self, encMessage):
        self.printText(self.username, self.decrypt(encMessage), "R")
        self.sendData(self.username, encMessage)
        #self.recieve_open=True
        #self.recieve_text()  
        #print("enc: "+str(encMessage))
        #self.recieve_text()

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

    #Server Communication+Handling
                
    def listen(self):
        while True: 
            try:   
                self.received=self.c.recv(4096)
                if str(self.received)[2]=="!":
                    print(f"Error from Server: {str(self.received)}")
                    self.text_insert(self.message_log, f"\nError from Server: {str(self.received)[2:-1]}")
                    self.text_insert(self.message_log, f"\nPlease Restart the clint with a new Username")
                    break
                else:
                    self.receivedL=self.received.split(b"\0")
                    print(self.received)
                    print(f"Bytes received: {self.received}")
                    #print(self.receivedL)
                    if self.username!=str(self.receivedL[0])[2:-1]:
                        self.printText(str(self.receivedL[0])[2:-1], self.decrypt(self.receivedL[1]))
                    
                
                """if not isinstance(self.received, (list, tuple)):
                    try:
                        if self.received[2]=="!":
                            print(f"Error from Server: {self.received}")
                    except IndexError:
                        print("Error: Unexpected data received from server")
                    """
                #response=response.decode("utf-8")
                #print(f"{response}")
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
                break
            except Exception as e:
                print(f"ClientSide error: {e}")
                break
        self.c.close()
        print("client closed")
            
    def sendData(self, username, data):
        """dataL2=data.split("|")
        dataL2.insert(0, username.)
        print(dataL2)
        dataL=[]
        for x in dataL2:
            dataL.append(username.encode("utf-8"))"""

        dataL=[]
        dataL.append(username.encode("utf-8"))   
        dataL.append(data)
        #print(dataL)
        send_this=b""
        for x in dataL:
            send_this += x
            send_this += b"\0"
        print(f"Bytes Sent: {send_this}")
        try: 
            self.c.send(send_this)
        except:
            self.text_insert(self.message_log, "\n YOU ARE NOT CONNECTED TO A SERVER. PLEASE CLOSE AND RECONNECT")
            print(' YOU ARE NOT CONNECTED TO A SERVER. PLEASE CLOSE AND RECONNECT')
                
    def handle_data(self):
        #print("test2")
        printed=False 
        while printed==False:
            try: 
                print("try")
                self.printText(str(self.received[0])[2:-1], self.decrypt(self.received[1]))
                print("good")
                printed=True
            except KeyboardInterrupt:
                print("Caught keyboard interrupt, exiting")
                break
            except:
                printed=False
        #print("PRINTJNG TEXTTTTTT")
        self.received=[]
        self.snd.recv_data=[]
                    
    #Encryption
      
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
        try:
            message = fkey.decrypt(encMessage).decode()
            return message
        except:
            print("closing sender")
            #self.c.send(f"close\0{str(self.received[0])[2:-1]}")
            print("You have recived a message with a non-compatable key. Please Disconnect, and reconnnect with the correct Key. ")
            self.text_insert(self.message_log, "\n You have recived a message with a non-compatable key. Please Disconnect, and reconnnect with the correct Key. ")
            self.c.send("closeme")
            self.c.close()
            self.restartClient()
            print("client closed")
    
    #Error Handling
    
    def restartClient(self):
        self.destroy()
        self.__init__        
    

if __name__ == "__main__":
    vsmp = VSMPClient("Kevin2","Banana1", "127.0.0.1", 42323)
    vsmp.recieve_open=True
    
    vsmp.mainloop()
    
    
    
    
    