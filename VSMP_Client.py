import tkinter as tk 
import tkinter.ttk as ttk

class VSMP_Client(tk.Tk):
    def __init__(self):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))



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
        textBox.insert(tk.END, insertmessage)
        textBox.config(state=tk.DISABLED)

    def getText(self):
        send_this=self.message.get("1.0", tk.END)
        self.message.delete("1.0", tk.END)
        self.text_insert(self.message_log, "\nUSERNAME: "+send_this)
        self.text_insert(self.message_log, "_____________________")
        print(send_this)

if __name__ == "__main__":
    vsmp = VSMP_Client()
    vsmp.mainloop()