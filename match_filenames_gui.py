import os
import re
import string
import tkinter as tk
from tkinter import messagebox, ttk

class BookMatcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("List Matcher")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.initialize_files()
        self.processed_names = self.load_processed()
        self.book_list = self.load_book_list()
        self.current_index = 0
        self.setup_gui()
        self.show_next_match()

    def initialize_files(self):
        if not os.path.exists("additions.txt"):
            open("additions.txt", 'w').close()
        if not os.path.exists("processed_filenames.txt"):
            messagebox.showerror("Error", "processed_filenames.txt not found")
            self.root.destroy()
        if not os.path.exists("book_list.txt"):
            messagebox.showerror("Error", "book_list.txt not found")
            self.root.destroy()

    def load_processed(self):
        with open("processed_filenames.txt", 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def load_book_list(self):
        with open("book_list.txt", 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.current_label = ttk.Label(
            main_frame, 
            font=('Arial', 10, 'bold'),
            text="Current title:")
        self.current_label.pack(anchor=tk.W, pady=5)
        # Matches listbox
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.matches_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.SINGLE, 
            height=8,
            font=('Arial', 10))
        self.matches_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.matches_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.matches_listbox.yview)
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(
            btn_frame, 
            text="Skip", 
            command=self.skip_match
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, 
            text="Select", 
            command=self.select_match
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, 
            text="No Match", 
            command=self.no_match
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, 
            text="Exit", 
            command=self.on_exit
        ).pack(side=tk.RIGHT)

    def find_matches(self, words):
        matches = []
        trans_table = str.maketrans({char: " " for char in string.punctuation})
        search_tokens = [w.lower() for w in words if w.strip()]
        for idx, line in enumerate(self.book_list):
            line_tokens = line.lower().translate(trans_table).split()
            if any(token in line_tokens for token in search_tokens):
                matches.append((line, idx))
        return matches

    def show_next_match(self):
        if self.current_index >= len(self.processed_names):
            messagebox.showinfo("Complete", "All titles processed!")
            self.on_exit()
            return
        current_title = self.processed_names[self.current_index]
        self.current_label.config(text=f"Current title: {current_title}")
        self.matches_listbox.delete(0, tk.END)
        matches = self.find_matches(current_title.split())
        self.current_matches = matches
        if not matches:
            self.matches_listbox.insert(tk.END, "No automatic matches found")
            self.matches_listbox.config(state=tk.DISABLED)
        else:
            for line, _ in matches:
                self.matches_listbox.insert(tk.END, line)
            self.matches_listbox.config(state=tk.NORMAL)
            if matches:
                self.matches_listbox.selection_set(0)

    def modify_line(self, line):
        line = line.rstrip()
        if line.endswith(' -'):
            return line
        elif line.endswith(' b') or line.endswith(' *'):
            return line[:-2] + ' -'
        return line + ' -'

    def select_match(self):
        if not self.current_matches:
            messagebox.showerror("Error", "No matches available to select!")
            return
        if not self.matches_listbox.curselection():
            messagebox.showerror("Error", "Please select a match first!")
            return
        
        selected_idx = self.matches_listbox.curselection()[0]
        original_line, book_idx = self.current_matches[selected_idx]
        modified_line = self.modify_line(original_line)
        self.book_list[book_idx] = modified_line
        self.save_book_list()  # Immediate save
        self.current_index += 1
        self.show_next_match()

    def no_match(self):
        current_title = self.processed_names[self.current_index]
        try:
            with open("additions.txt", 'a', encoding='utf-8') as f:
                f.write(f"{current_title}\n")
            self.current_index += 1
            self.show_next_match()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write to additions.txt: {str(e)}")

    def save_book_list(self):
        try:
            with open("book_list.txt", 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.book_list))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save book_list.txt: {str(e)}")

    def skip_match(self):
        self.current_index += 1
        self.show_next_match()

    def on_exit(self):
        self.save_book_list()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookMatcherGUI(root)
    root.mainloop()

