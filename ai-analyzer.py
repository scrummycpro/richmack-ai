import tkinter as tk
from tkinter import ttk, filedialog
import ollama
import sqlite3
from datetime import datetime

class DocumentAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Analyzer")
        self.geometry("400x300")

        self.file_path = None

        self.file_label = ttk.Label(self, text="Select a document to analyze:")
        self.file_label.pack(pady=10)

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.analyze_button = ttk.Button(self, text="Analyze", command=self.analyze_document)
        self.analyze_button.pack(pady=5)

        self.result_label = ttk.Label(self, text="")
        self.result_label.pack(pady=10)

        # SQLite database connection
        self.conn = sqlite3.connect('document_analysis.db')
        self.create_table()

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS analysis_results
                         (id INTEGER PRIMARY KEY,
                         document TEXT,
                         analysis_result TEXT,
                         timestamp TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            self.file_label.config(text=f"Selected document: {self.file_path}")

    def analyze_document(self):
        if self.file_path:
            with open(self.file_path, "r") as file:
                document_content = file.read()

            response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': document_content}])
            analysis_result = response['message']['content']

            self.result_label.config(text=f"Analysis result: {analysis_result}")

            # Save analysis result to SQLite database
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_to_database(document_content, analysis_result, timestamp)
        else:
            tk.messagebox.showinfo("Error", "Please select a document first.")

    def save_to_database(self, document_content, analysis_result, timestamp):
        c = self.conn.cursor()
        c.execute("INSERT INTO analysis_results (document, analysis_result, timestamp) VALUES (?, ?, ?)",
                  (document_content, analysis_result, timestamp))
        self.conn.commit()

if __name__ == "__main__":
    app = DocumentAnalyzerApp()
    app.mainloop()
