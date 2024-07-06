from scoreboard import draw_score_board, check_turn, check_for_win
import os

board = {1 : '1', 2 : '2',  3 : '3', 4 : '4', 5 : '5',  6 : '6',7 : '7', 8 : '8',  9 : '9'}

# draw_score_board(board)

isPlaying = True
isGameOver = False
player_turn = 0
last_turn = -1

while isPlaying:
    os.system('cls' if os.name == 'nt' else 'clear')
    draw_score_board(board)
    if last_turn == player_turn:
        print("invalid move selected, please try again.")
    last_turn = player_turn

    print(f"(Enter number between 0 to 9 or press 'q' to quit)\nPlayer {str((player_turn % 2) + 1)}'s turn: ")

    # get input from player
    moves = input()
    if moves == 'q':
        isPlaying = False
    elif str.isdigit(moves) and int(moves) in board:
        # checks if moves already taken
        if not board[int(moves)] in ["X", "O"]:
            player_turn += 1
            board[int(moves)] = check_turn(player_turn)
    
    if check_for_win(board):
        isPlaying = False
        isGameOver = True
    if player_turn > 8:
        player_turn = False

# print result
os.system('cls' if os.name == 'nt' else 'clear')
draw_score_board(board)

if isGameOver:
    if check_turn(player_turn) == 'X':
        print('Player X Wins!')
    else:
        print('Player O Wins!')
else:
    print('No Winner!')

print('Game Over!')