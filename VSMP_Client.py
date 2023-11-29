import tkinter as tk 
import tkinter.ttk as ttk

client_window=tk.Tk()
client_window.title("VSMP")
client_window.geometry("600x625")
client_window.minsize(width=300, height=625)
message_frame=tk.Frame(master=client_window, bg="pink", padx=25, pady=25)


greeting = tk.Label(master=message_frame, text="YOU ARE CHATTING WITH:")
message= tk.Text(master=message_frame, width=20)
recieve= tk.Entry(master=message_frame, width=20)
send=tk.Button(master=message_frame, text="SEND", padx=50, pady=25, bg="blue")  

message_frame.columnconfigure([0,2], weight=1)
message_frame.rowconfigure([0,2], weight=1)

message_frame.pack(padx=25, pady=25, fill=tk.Y)

greeting.grid(column=0, row=0, sticky=tk.N, pady=10, columnspan=2)
message.grid(column=1, row=1, sticky=tk.W)
recieve.grid(column=0, row=1, sticky=tk.E)
send.grid(column=0, row=2, sticky=tk.S, pady=15, columnspan=2)

message_var=message.get("1.0", tk.END)

client_window.mainloop()