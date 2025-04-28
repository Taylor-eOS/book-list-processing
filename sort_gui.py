import tkinter as tk
from collections import deque
from itertools import combinations
import random

class SortingApp:
    def __init__(self, root, lines):
        self.root = root
        self.lines = list(set(lines))  # Remove duplicates
        random.shuffle(self.lines)     # Avoid input order bias
        
        self.dag = {line: set() for line in self.lines}
        self.undetermined_pairs = set(combinations(self.lines, 2))
        self.current_pair = None
        self.sorted_lines = []

        self.setup_gui()
        self.next_pair()

    def setup_gui(self):
        self.root.title("Interactive Sorter")
        
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack()

        # Question label
        self.question_label = tk.Label(
            self.main_frame,
            text="Which item should come first?",
            font=('Arial', 14)
        )
        self.question_label.pack(pady=10)

        # Options frame
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(pady=20)

        # Left option
        self.left_button = tk.Button(
            self.options_frame,
            text="", 
            width=20,
            height=3,
            command=lambda: self.process_choice(0)
        )
        self.left_button.pack(side=tk.LEFT, padx=10)

        # Right option
        self.right_button = tk.Button(
            self.options_frame,
            text="",
            width=20,
            height=3,
            command=lambda: self.process_choice(1)
        )
        self.right_button.pack(side=tk.RIGHT, padx=10)

        # Progress label
        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 10))
        self.progress_label.pack(pady=10)

        # Key bindings
        self.root.bind('<Left>', lambda e: self.process_choice(0))
        self.root.bind('<Right>', lambda e: self.process_choice(1))

    def update_progress(self):
        total = len(self.undetermined_pairs) + len(self.sorted_lines) * (len(self.sorted_lines) - 1) // 2
        remaining = len(self.undetermined_pairs)
        self.progress_label.config(
            text=f"Progress: {total - remaining}/{total} comparisons made"
        )

    def next_pair(self):
        self.update_progress()
        
        while self.undetermined_pairs:
            pair = next(iter(self.undetermined_pairs), None)
            if not pair:
                break
            
            A, B = pair
            if self.reaches(A, B):
                self.undetermined_pairs.discard(pair)
                continue
            if self.reaches(B, A):
                self.undetermined_pairs.discard(pair)
                continue

            self.current_pair = (A, B)
            self.left_button.config(text=A, state=tk.NORMAL)
            self.right_button.config(text=B, state=tk.NORMAL)
            return

        # All pairs determined - sort and exit
        self.sorted_lines = self.topological_sort()
        with open('sorted_output.txt', 'w') as f:
            f.write('\n'.join(self.sorted_lines))
        self.root.destroy()

    def reaches(self, source, target):
        visited = set()
        queue = deque([source])
        while queue:
            node = queue.popleft()
            if node == target:
                return True
            if node not in visited:
                visited.add(node)
                queue.extend(self.dag[node])
        return False

    def process_choice(self, choice):
        if not self.current_pair:
            return

        A, B = self.current_pair
        if choice == 0:
            self.dag[A].add(B)
        else:
            self.dag[B].add(A)

        self.undetermined_pairs.discard(self.current_pair)
        self.current_pair = None
        self.left_button.config(state=tk.DISABLED)
        self.right_button.config(state=tk.DISABLED)
        self.root.after(100, self.next_pair)

    def topological_sort(self):
        in_degree = {node: 0 for node in self.lines}
        for node in self.lines:
            for neighbor in self.dag[node]:
                in_degree[neighbor] += 1

        queue = deque([node for node in self.lines if in_degree[node] == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)
            for neighbor in self.dag[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(self.lines):
            raise ValueError("Cycle detected - inconsistent user choices")
        return sorted_order

def main():
    # Read input file
    with open('input.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    root = tk.Tk()
    app = SortingApp(root, lines)
    root.mainloop()

if __name__ == "__main__":
    main()
