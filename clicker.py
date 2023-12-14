import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import customtkinter

toggle_key = KeyCode.from_char(char="ű")
mouse = Controller()
click_thread = None
clicking = False

def click_action():
    global clicking
    while clicking:
        mouse.click(Button.left, 1)
        time.sleep(0.01)

def on_press(key):
    global click_thread, clicking

    if key == toggle_key:
        if clicking:
            clicking = False
            if click_thread:
                click_thread.join()  # Wait for the click thread to finish
        else:
            clicking = True
            click_thread = threading.Thread(target=click_action)
            click_thread.start()

def save_toggle_key(entry, label, btn):
    global toggle_key
    try:
        new_key = KeyCode.from_char(char=entry.get())
        toggle_key = new_key
        label.configure(text=f"Current Toggle Key: {toggle_key.char}")
    except AttributeError:
        label.configure(text="Invalid key")

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("480x480")
app.title("Autoclicker")

# Label to display the current toggle key
toggle_key_label = customtkinter.CTkLabel(app, text=f"Current Toggle Key: {toggle_key.char}")
toggle_key_label.pack(padx=10, pady=10)

# Entry widget for user input
entry = customtkinter.CTkEntry(app)
entry.pack(padx=10, pady=10)

# Button to save the changes
save_btn = customtkinter.CTkButton(app, text="Save", command=lambda: save_toggle_key(entry, toggle_key_label, save_btn))
save_btn.pack(padx=10, pady=10)

# Start the keyboard listener in a separate thread
listener_thread = threading.Thread(target=Listener(on_press=on_press).start)
listener_thread.start()

app.mainloop()
