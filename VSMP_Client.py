import tkinter as tk 
import tkinter.ttk as ttk

client_window=tk.Tk()
client_window.title("VSMP")
client_window.geometry("400x400")

greeting = tk.Label(text="EnterMessage")
message= tk.Text(width="75", height="50")
send=tk.Button()

greeting.pack()
message.pack()
send.pack()

message_var=message.get("1.0", tk.END)

client_window.mainloop()