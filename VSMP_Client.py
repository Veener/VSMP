import tkinter as tk 
import tkinter.ttk as ttk

from cryptography.fernet import Fernet  
import hashlib
import base64

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
            self.fkey=self.gen_key(self.keyWord)

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

    def text_insert(self, textBox, insertmessage):
        textBox.config(state=tk.NORMAL)
        textBox.insert(tk.END,insertmessage)
        textBox.config(state=tk.DISABLED)

    def getText(self):
        send_this=self.message.get("1.0", tk.END)
        self.message.delete("1.0", tk.END)
        print("enc: "+str(self.encrypt(send_this)))
        self.sendText(str(self.encrypt(send_this)))
    
    def sendText(self, send_this):
        self.text_insert(self.message_log, "\n_____________________")
        self.text_insert(self.message_log, "\n"+self.username+": "+ self.decrypt(send_this))
        self.text_insert(self.message_log, "\n_____________________")
        print("dec: "+str(self.decrypt(send_this)))
        
    def gen_key(self, keyword):
        keyword_bytes = keyword.encode('utf-8')
        key_bytes = hashlib.sha256(keyword_bytes).digest()[:32]
        key = base64.urlsafe_b64encode(key_bytes)
        fkey = Fernet(key)
        self.fkey2=fkey
        return fkey
    
    def encrypt(self, message):
        encMessage = self.fkey.encrypt(message.encode())
        print(self.fkey2.decrypt(encMessage).decode())
        return encMessage
    
    def decrypt(self, encMessage):
        message = self.fkey.decrypt(encMessage).decode()
        return message
    

if __name__ == "__main__":
    vsmp = VSMPClient("Vinny","Banana")
    vsmp.mainloop()