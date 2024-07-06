def draw_score_board(board):
    score_board = (f"|{board[1]}|{board[2]}|{board[3]}|\n"
                   f"|{board[4]}|{board[5]}|{board[6]}|\n"
                   f"|{board[7]}|{board[8]}|{board[9]}|")
    print(score_board)

def check_turn(player_turn):
    if player_turn % 2 == 0:
        return 'O'
    else:
        return 'X'

def check_for_win(board):
    if (board[1] == board[2] == board[3] or board[4] == board[5] == board[6] or board[7] == board[8] == board[9]):
        return True

    elif (board[1] == board[4] == board[7] or board[2] == board[5] == board[8] or board[3] == board[6] == board[9]):
        return True

    elif (board[1] == board[5] == board[9] or board[3] == board[5] == board[7]):
        return True

    else:
        return False