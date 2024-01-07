import tkinter as tk
from tkinter import ttk


class IMDBMsg(tk.Toplevel):
    def __init__(self, parent, title, message):
        tk.Toplevel.__init__(self, parent)
        self.title(title)

        label = ttk.Label(self, text=message)
        label.pack(padx=10, pady=10)

        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10)

    @staticmethod
    def show_imdb_msg(parent, title, message):
        dialog = IMDBMsg(parent, title, message)
        parent.wait_window(dialog)
