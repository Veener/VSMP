import tkinter as tk 
import tkinter.ttk as ttk

class VSMP_Login(tk.Tk):
    def __init__(self):
            super().__init__()
            self.title("VSMP")
            #self.iconbitmap("D:/SpaceShuttle.ico")
            self.attributes("-topmost", 1)
            self.style=ttk.Style(self)
            self.style.configure("TButton", font=("Helvetica", 24))



            ww = 300
            wh = 150
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            cx = int(sw / 2 - ww / 2)
            cy = int(sh / 2 - wh / 2)
            self.geometry(f"{ww}x{wh}+{cx}+{cy}")
            self.minsize(width=300, height=150)
            self.login_frame()

    def login_frame(self):
        self.loginFrame=tk.Frame(master=self, bg="pink", padx=25, pady=25)

        self.username_text=tk.Label(master=self.loginFrame, text="Username:", bg="pink",)
        self.username_input=tk.Entry(master=self.loginFrame,)
        self.key_text=tk.Label(master=self.loginFrame, text="Key:", bg="pink",)
        self.key_input=tk.Entry(master=self.loginFrame,)

        self.login_button=tk.Button(master=self.loginFrame, text="Login")

        self.loginFrame.pack(padx=25, pady=25, fill=tk.BOTH)

        self.username_text.grid(row=0, column=0,)
        self.username_input.grid(row=0, column=1, columnspan=2)
        self.key_text.grid(row=1, column=0)
        self.key_input.grid(row=1, column=1, columnspan=2)
        self.login_button.grid(row=2, column=1, columnspan=2)
        
if __name__ == "__main__":
    go = VSMP_Login()
    go.mainloop()