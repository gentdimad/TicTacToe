
from zero import ZeroServer
import sqlite3

def init():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute("""
	SELECT name FROM sqlite_master WHERE type='table' AND name='data'
	""")
    if not cursor.fetchone():
        cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER, name TEXT, value TEXT)")
        cursor.execute("INSERT INTO data VALUES (1, 'users', '0')")
        cursor.execute("INSERT INTO data VALUES (2, 'board', '[[0, 0, 0], [0, 0, 0], [0, 0, 0]]')")
        cursor.execute("INSERT INTO data VALUES (3, 'current', '1')")
        connection.commit()
    connection.close()

# Handle button clicks
def handle_click(coords: tuple) -> str:

    if coords[2][coords[0]][coords[1]] == 0:
        if coords[3] == 1:
            coords[2][coords[0]][coords[1]] = "X"
            check = check_for_winner(coords[2])
            if (check == "Continue"):
                return "X"
            else:
                return check
        else:
            coords[2][coords[0]][coords[1]] = "O"
            check = check_for_winner(coords[2])
            if (check == "Continue"):
                return "O"
            else:
                return check

def connect_user() -> int:
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM data WHERE id= 1 AND value='0'")
    nousers = cursor.fetchall()

    if(len(nousers) == 1 ):
        cursor.execute("UPDATE data SET value='1' WHERE id = 1")
        connection.commit()
        connection.close()
        print(1)
        return 1
    
    #Check if user has entered
    cursor.execute("SELECT * FROM data WHERE id = 1 AND value = '1'")
    users = cursor.fetchall()

    if(len(users) == 1 ):
        cursor.execute("UPDATE data SET value = '2' WHERE id = 1")
        connection.commit()
        connection.close()
        print(2)
        return 2
    

#Check for a winner or a tie
def check_for_winner(board: list) -> str:
    winner = None

    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != 0:
            winner = row[0]
            break

    # Check columns
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            winner = board[0][col]
            break

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        winner = board[0][2]

    if all([all(row) for row in board]) and winner is None:
        winner = "tie"

    if winner:
        return declare_winner(winner)
    else:
        return "Continue"

# Declare the winner and ask to restart the game
def declare_winner(winner:str) -> str:
    if winner == "tie":
        return "It's a tie!"
    else:
        return f"Player {winner} wins!" 


if __name__ == "__main__":
    app = ZeroServer(port=5559)
    init()
    app.register_rpc(connect_user)
    app.register_rpc(handle_click)
    app.register_rpc(check_for_winner)
    app.register_rpc(declare_winner)
    app.run()