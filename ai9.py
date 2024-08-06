def printBoard(board):
    for row in board:
        print(" | ".join(row))
        print("- "*5)

def checkWin(board, player):
    conditions = [
        [board[0][0],board[0][1], board[0][2]],
        [board[1][0],board[1][1], board[1][2]],
        [board[2][0],board[2][1], board[2][2]],

        [board[0][0],board[1][0], board[2][0]],
        [board[0][1],board[1][1], board[2][1]],
        [board[0][2],board[1][2], board[2][2]],

        [board[0][0],board[1][1], board[2][2]],
        [board[0][2],board[1][1], board[2][0]],
    ]
    return [player,player,player] in conditions

def checkDraw(board):
    for row in board:
        if " " in row:
            return False
    return True

def tictactoe():
    board = [[" "for _ in range(3)]for _ in range(3)]
    current = "X"

    while(True):
        printBoard(board)

        row = int(input(f"Player {current} enter row: "))
        col = int(input(f"Player {current} enter col: "))

        if board[row][col] == " ":
            board[row][col] = current
        else:
            print("Spot already taken!")
            continue
        if checkWin(board, current):
            printBoard(board)
            print(f"Player {current} wins!!")
            break
        if checkDraw(board):
            printBoard(board)
            print("Its a draw")
            break
        current = "O" if current=="X" else "X"

tictactoe()
