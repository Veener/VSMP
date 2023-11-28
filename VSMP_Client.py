import tkinter as tk 
import tkinter.ttk as ttk

client_window=tk.Tk()
client_window.title("VSMP")
client_window.geometry("600x600")

message_frame=tk.Frame(master=client_window, bg="pink")


greeting = tk.Label(master=message_frame, text="YOU ARE CHATTING WITH:")
message= tk.Text(master=message_frame)
send=tk.Button(master=message_frame, text="SEND", padx=50, pady=25)  

message_frame.columnconfigure([0,2], weight=1)
message_frame.rowconfigure([0,2], weight=1)

message_frame.pack(padx=25, pady=25, fill=tk.BOTH)

greeting.grid(column=0, row=0)
message.grid(column=0, row=1,sticky='nswe')
send.grid(column=0, row=2)

message_var=message.get("1.0", tk.END)

client_window.mainloop()