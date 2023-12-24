from tkinter import Tk, Button, Frame, Text

# Define window width and element proportions
WINDOW_WIDTH = 500
TOTAL_COLUMNS = 8

# Calculate column widths based on proportions and total columns
restart_width = int(WINDOW_WIDTH * 0.25 / TOTAL_COLUMNS)
text_width = int(WINDOW_WIDTH * 0.50 / TOTAL_COLUMNS)
save_width = load_width = int(WINDOW_WIDTH * 0.125 / TOTAL_COLUMNS)

# Create the main window and taskbar frame
root = Tk()
root.geometry(f"{WINDOW_WIDTH}x30")
taskbar_frame = Frame(root)
taskbar_frame.pack(fill="x")

# Create and pack button frames with padding
restart_frame = Frame(taskbar_frame)
restart_frame.pack(side="left", expand=True)
restart_button = Button(restart_frame, text="Restart", width=restart_width)
restart_button.pack(expand=True, pady=5)

text_frame = Frame(taskbar_frame)
text_frame.pack(side="left", expand=True)
text_box = Text(text_frame, width=text_width)
text_box.pack(expand=True, pady=5)

save_frame = Frame(taskbar_frame)
save_frame.pack(side="left", expand=True)
save_button = Button(save_frame, text="Save", width=save_width)
save_button.pack(expand=True, pady=5)

load_frame = Frame(taskbar_frame)
load_frame.pack(side="left", expand=True)
load_button = Button(load_frame, text="Load", width=load_width)
load_button.pack(expand=True, pady=5)
gen="funnny"
print("\0"+gen)

# Start the main loop
root.mainloop()
