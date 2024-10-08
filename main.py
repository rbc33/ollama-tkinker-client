import tkinter as tk
from tkinter import OptionMenu, Scrollbar, StringVar, Text, Entry, Button
import json
import threading
from langchain_community.llms.ollama import Ollama
from ollama_list import list_models


BASE_URL = "http://192.168.0.100:11434"

# Variable global para almacenar el modelo seleccionado
SELECTED_MODEL = "llama3.1"


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Chat Interface")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.geometry("600x700")

        # Frame para el dropdown
        dropdown_frame = tk.Frame(root)
        dropdown_frame.grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(10, 0), padx=10
        )

        # Dropdown menu
        self.options = list_models()
        self.clicked = StringVar()
        self.clicked.set(SELECTED_MODEL)
        self.clicked.trace("w", self.update_selected_model)

        self.drop = OptionMenu(dropdown_frame, self.clicked, *self.options)
        self.drop.config(width=20)
        self.drop.pack(side="left")

        # Chat area
        self.chat_area = Text(root, wrap="word", state="disabled", width=40, height=20)
        self.chat_area.grid(
            row=1, column=0, padx=(10, 10), pady=10, columnspan=3, sticky="nsew"
        )

        # Scrollbar
        scrollbar = Scrollbar(root, command=self.chat_area.yview)
        scrollbar.grid(row=1, column=3, sticky="nsew")
        self.chat_area["yscrollcommand"] = scrollbar.set

        # Entry field
        self.entry_field = Entry(root)
        self.entry_field.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="ew")
        self.entry_field.bind("<Return>", self.send_message)

        # Send button
        send_button = Button(root, text="Enviar", command=self.send_message)
        send_button.grid(row=2, column=1, pady=10)

    def update_selected_model(self, *args):
        global SELECTED_MODEL
        SELECTED_MODEL = self.clicked.get()
        self.display_message(f"Modelo seleccionado: {SELECTED_MODEL}")

    def send_message(self, event=None):
        user_input = self.entry_field.get()
        if user_input:
            self.display_message(f"Usuario: {user_input}")
            threading.Thread(
                target=self.generate_and_display,
                args=(SELECTED_MODEL, user_input),
                daemon=True,
            ).start()
            self.entry_field.delete(0, "end")

    def display_message(self, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", message + "\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def generate_and_display(self, model_name, prompt):
        try:
            lm = Ollama(model=model_name)
            response = lm.invoke(prompt)
            self.root.after(0, self.display_message, f"Respuesta: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.root.after(0, self.display_message, "Error al procesar el mensaje")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
