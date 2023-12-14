import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import customtkinter

toggle_key = KeyCode.from_char(char="0")
mouse = Controller()
click_thread = None
clicking = False
click_frequency = 0.01 

def click_action():
    global clicking, click_frequency
    while clicking:
        mouse.click(Button.left, 1)
        time.sleep(click_frequency)

def on_press(key):
    global click_thread, clicking

    if key == toggle_key:
        if clicking:
            clicking = False
            if click_thread:
                click_thread.join()
        else:
            clicking = True
            click_thread = threading.Thread(target=click_action)
            click_thread.start()

def save_toggle_key(entry, label1, btn, frequency_slider, label2):
    global toggle_key, click_frequency
    try:
        new_key = KeyCode.from_char(char=entry.get())
        toggle_key = new_key
        label1.configure(text=f"Current Toggle Key: {toggle_key.char}")
    except AttributeError:
        label1.configure(text="Invalid key")

    click_frequency = frequency_slider.get()
    label2.configure(text=f"Frequency: {round(click_frequency, 6)}s")
    print(f"Click frequency set to: {click_frequency}")




customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("480x480")
app.title("Autoclicker")

toggle_key_label = customtkinter.CTkLabel(app, text=f"Current Toggle Key: {toggle_key.char}")
toggle_key_label.pack(padx=10, pady=10)

entry = customtkinter.CTkEntry(app)
entry.insert(0, "0")
entry.pack(padx=10, pady=10)

save_btn = customtkinter.CTkButton(app, text="Save", command=lambda: save_toggle_key(entry, toggle_key_label, save_btn, frequency_slider, frequency_label))
save_btn.pack(padx=10, pady=10)

frequency_slider = customtkinter.CTkSlider(app, from_=1, to=0.00001)
frequency_slider.set(0.1)
frequency_slider.pack(padx=10, pady=10)

frequency_label = customtkinter.CTkLabel(app, text=f"Frequency: {click_frequency}s")
frequency_label.pack(padx=10, pady=10)

listener_thread = threading.Thread(target=Listener(on_press=on_press).start)
listener_thread.start()

app.mainloop()
