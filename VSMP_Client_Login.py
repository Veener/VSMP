import tkinter as tk 
import tkinter.ttk as ttk
from VSMP_ClientV3 import VSMPClient 

class VSMP_Login(tk.Tk):
    def __init__(self):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))



            ww = 300
            wh = 200
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = int(sw / 2 - ww / 2)
            cy = int(sh / 2 - wh / 2)
            self.geometry(f"{ww}x{wh}+{cx}+{cy}")
            self.minsize(width=300, height=150)
            print("t1")
            self.login_frame()

    def login_frame(self):
        print("t2")
        self.loginFrame=tk.Frame(master=self, bg="pink", padx=25, pady=25)

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
        self.key=self.key_input.get()
        self.host=self.host_input.get()
        self.port=self.port_input.get()
        global loginInfo
        loginInfo=[]
        loginInfo=[self.username, self.key, self.host, self.port]
        
        
if __name__ == "__main__":
    go = VSMP_Login()
    go.mainloop()