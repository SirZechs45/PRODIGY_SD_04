import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.sudoku_values = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(master, width=3, font=('Arial', 14), textvariable=self.sudoku_values[i][j])
                entry.grid(row=i, column=j)
                entry.bind('<FocusIn>', lambda event, i=i, j=j: self.clear_entry(i, j))

        solve_button = tk.Button(master, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, pady=10)

    def clear_entry(self, i, j):
        self.sudoku_values[i][j].set("")

    def solve(self):
        sudoku_board = [[0] * 9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    value = self.sudoku_values[i][j].get()
                    if value and 1 <= int(value) <= 9:
                        sudoku_board[i][j] = int(value)
                    elif value:
                        raise ValueError("Value must be between 1 and 9")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input at row {} and column {}".format(i + 1, j + 1))
                    return

        if self.solve_sudoku(sudoku_board):
            # Update the GUI with the solved Sudoku
            for i in range(9):
                for j in range(9):
                    self.sudoku_values[i][j].set(sudoku_board[i][j])
        else:
            messagebox.showerror("Error", "No solution found for the given Sudoku puzzle")

    def solve_sudoku(self, board):
        empty = self.find_empty_location(board)
        if not empty:
            return True  # Puzzle solved

        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num

                if self.solve_sudoku(board):
                    return True

                board[row][col] = 0  # Backtrack if no solution found

        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_safe(self, board, row, col, num):
        return (
            not self.used_in_row(board, row, num)
            and not self.used_in_col(board, col, num)
            and not self.used_in_box(board, row - row % 3, col - col % 3, num)
        )

    def used_in_row(self, board, row, num):
        return num in board[row]

    def used_in_col(self, board, col, num):
        return num in [board[i][col] for i in range(9)]

    def used_in_box(self, board, start_row, start_col, num):
        return any(num in board[i][start_col : start_col + 3] for i in range(start_row, start_row + 3))

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
