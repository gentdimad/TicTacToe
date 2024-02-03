from zero import ZeroClient
import tkinter as tk
from tkinter import messagebox

zero_client = ZeroClient("localhost", 5559)

current_player = 1
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def connect():
    resp = zero_client.call("connect_user", None)
    print(resp)

def create_board(window):

    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", font=("Arial", 50), height=2, width=6, bg="lightblue", command=lambda row=i, col=j: handle_click(row, col))
            button.grid(row=i, column=j, sticky="nsew")

def handle_click(row, col):
    global board
    global current_player

    check = zero_client.call("handle_click", (row, col, board, current_player))
    if (check == "X" or check == "O"):
        button = window.grid_slaves(row=row, column=col)[0]
        button.config(text=check)
        if (check == "X"):
            board[row][col] = check
            current_player = 2
        elif (check == "O"):
            board[row][col] = check
            current_player = 1
    else:
        if (current_player == 1):
            button = window.grid_slaves(row=row, column=col)[0]
            button.config(text="X")
            board[row][col] = "X"
        else:
            button = window.grid_slaves(row=row, column=col)[0]
            button.config(text=")")
            board[row][col] = "O"

        answer = messagebox.showinfo("Game Over", check)


if __name__ == "__main__":
    connect()
    window = tk.Tk()
    window.title("Tic Tac Toe")
    create_board(window)
    window.mainloop()
