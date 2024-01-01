import time
import pyautogui
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import keyboard

class KeystrokeSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tenebris.dsc")

        self.sentence_var = tk.StringVar(value="Lux fit tenebrae. Tenebrarum fit inanis")
        self.stop_simulation_flag = threading.Event()
        self.spam_sentence_var = tk.StringVar(value="Spam this sentence")
        self.stop_spam_flag = threading.Event()

        self.display_instructions()

        self.create_tabs()

        keyboard.on_press_key('esc', self.stop_all)

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        simulator_tab = ttk.Frame(tab_control)
        self.create_simulator_tab(simulator_tab)
        tab_control.add(simulator_tab, text="Deleter")

        spammer_tab = ttk.Frame(tab_control)
        self.create_spammer_tab(spammer_tab)
        tab_control.add(spammer_tab, text="Spammer")

        tab_control.pack(expand=1, fill="both")

    def create_simulator_tab(self, parent):
        ttk.Label(parent, text="Final Message:").pack(pady=5)
        self.sentence_entry = ttk.Entry(parent, textvariable=self.sentence_var, width=40)
        self.sentence_entry.pack(pady=5)

        start_button = ttk.Button(parent, text="Delete", command=self.start_simulation)
        start_button.pack(pady=10)

    def create_spammer_tab(self, parent):
        ttk.Label(parent, text="Enter Sentence to Spam:").pack(pady=5)
        spam_sentence_entry = ttk.Entry(parent, textvariable=self.spam_sentence_var, width=40)
        spam_sentence_entry.pack(pady=5)

        spam_button = ttk.Button(parent, text="Spam", command=self.start_spam)
        spam_button.pack(pady=10)

    def start_simulation(self):
        sentence = self.sentence_var.get()

        def simulate():
            time.sleep(1)
            pyautogui.write(sentence, interval=0.01)
            pyautogui.press('enter')
            time.sleep(5)

            while not self.stop_simulation_flag.is_set():
                pyautogui.press('up')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(0.35)

        self.stop_simulation_flag.clear()
        threading.Thread(target=simulate, daemon=True).start()

    def stop_simulation(self):
        self.stop_simulation_flag.set()

    def start_spam(self):
        spam_sentence = self.spam_sentence_var.get()
        time.sleep(2)

        def spam():
            while not self.stop_spam_flag.is_set():
                pyautogui.write(spam_sentence, interval=0.02)
                pyautogui.press('enter')
                time.sleep(0.15)

        self.stop_spam_flag.clear()
        threading.Thread(target=spam, daemon=True).start()

    def stop_spam(self):
        self.stop_spam_flag.set()

    def stop_all(self, e=None):
        self.stop_simulation()
        self.stop_spam()

    def display_instructions(self):
        instructions = "Welcome to Tenebris.dsc!\n\n"
        instructions += "Instructions:\n"
        instructions += "- To start the Deleter, enter the final message and click 'Delete'.\n"
        instructions += "      - Than click in the Discord Message bar within 3 seconds to start deleting.\n\n"
        instructions += "- To start spamming, enter the sentence to spam and click 'Spam'.\n"
        instructions += "      - Than click in the Discord Message bar within 3 seconds to start spaming.\n\n"
        instructions += "- Press 'Esc' key to stop the Deleter or Spammer at any time."

        messagebox.showinfo("Instructions", instructions)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeSimulatorGUI(root)
    root.geometry("500x300")  # Set the initial size of the window
    root.mainloop()
