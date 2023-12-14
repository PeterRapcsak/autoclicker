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

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("480x480")
app.title("Autoclicker")

btn = customtkinter.CTkButton(app, text="Save", command=lambda: None)  # No need for command now
btn.pack(padx=10, pady=10)

# Start the keyboard listener in a separate thread
listener_thread = threading.Thread(target=Listener(on_press=on_press).start)
listener_thread.start()

app.mainloop()
