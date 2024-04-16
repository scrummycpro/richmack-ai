import tkinter as tk
from tkinter import filedialog
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WordCloudGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Word Cloud Generator")

        self.text_entry = tk.Text(self, height=10, width=50)
        self.text_entry.pack(pady=10)

        self.upload_button = tk.Button(self, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        self.generate_button = tk.Button(self, text="Generate Word Cloud", command=self.generate_wordcloud)
        self.generate_button.pack(pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.text_entry.delete('1.0', tk.END)
                self.text_entry.insert(tk.END, text)

    def generate_wordcloud(self):
        text = self.text_entry.get('1.0', tk.END)
        if text.strip() == "":
            tk.messagebox.showwarning("Empty Text", "Please enter some text or upload a file.")
            return

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    app = WordCloudGenerator()
    app.mainloop()
