import tkinter as tk
from tkinter import ttk
import random

class VisualSorter:
    def __init__(self, root, lines):
        self.root = root
        self.working_list = lines.copy()
        self.to_visit = self.working_list.copy()
        self.current_focus = 0
        self.setup_gui()
        self.pick_new_focus()

    def setup_gui(self):
        self.root.title("List Editor")
        self.root.geometry("1200x900")
        self.root.configure(bg="#ffffff")
        self.custom_font = ("Segoe UI", 11)
        self.bold_font = ("Segoe UI", 12, "bold")
        self.header_frame = tk.Frame(self.root, bg="#4090ff", height=60)
        self.header_frame.pack(fill=tk.X, pady=(0,10))
        self.current_label = tk.Label(
            self.header_frame,
            text="",
            font=self.bold_font,
            bg="#4090ff",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=10)
        self.current_label.pack()
        self.current_label.bind("<Button-1>", lambda e: self.pick_new_focus())
        self.container = tk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)
        self.root.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def create_gap(self, parent, insert_pos):
        gap = tk.Frame(parent, height=30, bg="#f0f0f0", cursor="hand2")
        gap.bind("<Enter>", lambda e: gap.config(bg="#d0d0d0"))
        gap.bind("<Leave>", lambda e: gap.config(bg="#f0f0f0"))
        gap.bind("<Button-1>", lambda e, pos=insert_pos: self.move_current_item(pos))
        gap.pack(fill=tk.X, pady=0)
        return gap

    def draw_context(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        for i, val in enumerate(self.working_list):
            item_frame = tk.Frame(self.scrollable_frame, bg="white")
            lbl = tk.Label(item_frame, text=val, font=self.custom_font, bg="#ffffff", fg="#333333", padx=20, pady=8, anchor="w", width=60)
            lbl.pack(fill=tk.X)
            if i == self.current_focus:
                item_frame.config(bg="#fff3d6")
                lbl.config(bg="#fff3d6", font=self.bold_font)
                lbl.bind("<Button-1>", lambda e: self.pick_new_focus())
                lbl.config(cursor="hand2")
            else:
                lbl.config(cursor="arrow")
            item_frame.pack(fill=tk.X)
            if i < len(self.working_list) - 1:
                self.create_gap(self.scrollable_frame, i + 1)
        self.canvas.update_idletasks()
        idx = 2 * self.current_focus
        y = self.scrollable_frame.winfo_children()[idx].winfo_y()
        h = self.canvas.winfo_height()
        total = self.scrollable_frame.winfo_height()
        self.canvas.yview_moveto(max(0, min(1, (y - h//2) / total)))

    def move_current_item(self, new_pos):
        if self.current_focus == new_pos:
            return
        item = self.working_list.pop(self.current_focus)
        if new_pos > self.current_focus:
            new_pos -= 1
        self.working_list.insert(new_pos, item)
        with open("input.txt", "w") as f:
            f.write("\n".join(self.working_list))
        self.current_focus = new_pos
        self.pick_new_focus()

    def pick_new_focus(self):
        if not self.to_visit:
            self.to_visit = self.working_list.copy()
        item = random.choice(self.to_visit)
        self.to_visit.remove(item)
        self.current_focus = self.working_list.index(item)
        self.current_label.config(text=item)
        self.draw_context()

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]
    root = tk.Tk()
    VisualSorter(root, lines)
    root.mainloop()

if __name__ == "__main__":
    main()

