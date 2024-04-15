import tkinter as tk
from tkinter import ttk
import ollama
import sqlite3
from datetime import datetime
from tkinter import filedialog

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat App")
        self.geometry("400x500")

        self.chat_history = []

        self.chat_frame = ttk.Frame(self)
        self.chat_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.chat_history_text = tk.Text(self.chat_frame, wrap="word")
        self.chat_history_text.pack(fill=tk.BOTH, expand=True)

        self.message_entry = ttk.Entry(self)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.send_button = ttk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.save_button = ttk.Button(self, text="Save", command=self.save_history)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        self.conn = sqlite3.connect('chat_history.db')
        self.create_table()

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                         (id INTEGER PRIMARY KEY,
                         sender TEXT,
                         message TEXT,
                         timestamp TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def send_message(self):
        user_message = self.message_entry.get()
        self.add_to_chat_history("You", user_message)

        response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': user_message}])
        bot_response = response['message']['content']

        self.add_to_chat_history("Bot", bot_response)

        self.message_entry.delete(0, tk.END)

        # Save chat history to database
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.save_to_database("You", user_message, timestamp)
        self.save_to_database("Bot", bot_response, timestamp)

    def add_to_chat_history(self, sender, message):
        chat_entry = f"{sender}: {message}\n"
        self.chat_history.append(chat_entry)
        self.chat_history_text.insert(tk.END, chat_entry)

    def save_to_database(self, sender, message, timestamp):
        c = self.conn.cursor()
        c.execute("INSERT INTO chat_history (sender, message, timestamp) VALUES (?, ?, ?)",
                  (sender, message, timestamp))
        self.conn.commit()

    def save_history(self):
        bot_responses = [chat_entry for chat_entry in self.chat_history if chat_entry.startswith("Bot")]
        for i, response in enumerate(bot_responses, 1):
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialfile=f"bot_response_{i}.txt")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(response)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
