import tkinter as tk 
import tkinter.ttk as ttk

client_window=tk.Tk()
client_window.title("VSMP")
client_window.geometry("600x625")
client_window.minsize(width=300, height=625)
message_frame=tk.Frame(master=client_window, bg="pink", padx=25, pady=25)

def getText():
    send_this=message.get("1.0", tk.END)
    message.delete("1.0", tk.END)
    text_insert(message_log, "\nUSERNAME: "+send_this)
    print(send_this)

def text_insert(textBox, insertmessage):
    textBox.config(state=tk.NORMAL)
    textBox.insert(tk.END, insertmessage)
    textBox.config(state=tk.DISABLED)


greeting = tk.Label(master=message_frame, text="YOU ARE CHATTING WITH:")
message= tk.Text(master=message_frame, height=5)
message_log= tk.Text( master=message_frame, height=15, yscrollcommand=True)
send=tk.Button(master=message_frame, text="SEND", padx=50, pady=25, bg="blue", command=lambda:getText())  

text_insert(message_log, "THIS IS A MESSAGE AHHH OMG YOU GOT MAILLLLLL")

message_frame.columnconfigure([0,1], weight=1)
message_frame.rowconfigure([0,3], weight=1)


message_frame.pack(padx=25, pady=25, fill=tk.BOTH)

greeting.grid(column=0, row=0, sticky=tk.N, pady=10)
message_log.grid(column=0, row=1)
message.grid(column=0, row=2,)
send.grid(column=0, row=3, sticky=tk.S, pady=15)

client_window.mainloop()