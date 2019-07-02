import urllib.request
import sys
import random
import time
from math import inf
import copy

# Returns a list of positions available on a board
def get_available_moves(board, player):
    l = []
    
   
    for column in range(len(board)):
        for line in range(len(board[column])):
            if board[column][line] == 0:
                    #if (column + 1, line + 1) != forbidden_moves:
                l.append((column + 1, line + 1))
    return l


# Check if a board is in an end-game state. Returns the winning player or None.
def is_final_state(board):
    # test vertical
    for column in range(len(board)):
        s = ""
        for line in range(len(board[column])):
            state = board[column][line]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2

    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[4]

    return None


# Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
# None at any of those places where there's no neighbor
def neighbors(board, column, line):
    l = []

    if line > 1:
        l.append((column, line - 1))  # up
    else:
        l.append(None)

    if (column < 6 or line > 1) and (column < len(board)):
        if column >= 6:
            l.append((column + 1, line - 1))  # upper right
        else:
            l.append((column + 1, line))  # upper right
    else:
        l.append(None)
    if (column > 6 or line > 1) and (column > 1):
        if column > 6:
            l.append((column - 1, line))  # upper left
        else:
            l.append((column - 1, line - 1))  # upper left
    else:
        l.append(None)

    if line < len(board[column - 1]):
        l.append((column, line + 1))  # down
    else:
        l.append(None)

    if (column < 6 or line < len(board[column - 1])) and column < len(board):
        if column < 6:
            l.append((column + 1, line + 1))  # down right
        else:
            l.append((column + 1, line))  # down right
    else:
        l.append(None)

    if (column > 6 or line < len(board[column - 1])) and column > 1:
        if column > 6:
            l.append((column - 1, line + 1))  # down left
        else:
            l.append((column - 1, line))  # down left
    else:
        l.append(None)

    return l

def heuristic(board, player):

    r_player1 = ["1", "11", "111", "1111"]
    r_player2 = ["2", "22", "222", "2222"]
    
    for col in range(0, len(board)):
        s = ""
        for line in range(len(board[col])):
            state = board[col][line]
            s += str(state)

            aux = 5 - len(s)
            total_line = 0
            for i in range(1, aux+1):
                total_line += board[col][line + i]

            if player == "1":
                if s in r_player1:                    
                    if total_line == 0:
                        return +10
                    else: 
                        return -10
            elif player == "2":
                if s in r_player2:                    
                    if total_line == 0: 
                        return +10
                    else: 
                        return -10            


    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)

            aux = 5 - len(s)
            total_line = 0

            coords_aux = neighbors(board, column, line)[1]
            for i in range(1, aux+1):
                if coords_aux != None:
                    column_aux = coords_aux[0]
                    line_aux = coords_aux[1]                
                    total_line += board[column_aux - 1][line_aux - 1]
                    coords_aux = neighbors(board, column_aux, line_aux)[1]
                else:
                    total_line = -1

            if player == "1":
                if s in r_player1:                    
                    if total_line == 0:
                        return +10
                    else: 
                        return -10
            elif player == "2":
                if s in r_player2:                    
                    if total_line == 0: 
                        return +10
                    else: 
                        return -10   
            coords = neighbors(board, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            
            aux = 5 - len(s)
            total_line = 0

            coords_aux = neighbors(board, column, line)[1]
            for i in range(1, aux+1):
                if coords_aux != None:
                    column_aux = coords_aux[0]
                    line_aux = coords_aux[1]                
                    total_line += board[column_aux - 1][line_aux - 1]
                    coords_aux = neighbors(board, column_aux, line_aux)[1]
                else:
                    total_line = -1

            if player == "1":
                if s in r_player1:                    
                    if total_line == 0:
                        return +10
                    else: 
                        return -10
            elif player == "2":
                if s in r_player2:                    
                    if total_line == 0: 
                        return +10
                    else: 
                        return -10  

            coords = neighbors(board, column, line)[4]

    return -5           


def minimax(board, depth, player, depth_initial, alpha=-inf, beta=inf, inv_move = (-1,-1)):
    """ 
    Minimax algorithm that choose the best movement in board
    Args:
        board (list): the state of the board
        depth (int): how many free position the board has
        player (str): player ("X" or "O") 
    Returns:
        tuple: score and best move
    """

    h = heuristic(board, player)
    #h = h + heuristic2(board, player)

    final_state = is_final_state(board)
    if final_state is not None:
        if final_state == 1:
            return -10 - depth, board
        else:
            return 10 + depth, board
    if depth == depth_initial-2:
        return h, board 


    if player == "2":
        best_val = inf
        best_mov = None
        for move in get_available_moves(board, player):
            #print(move)
            #print(get_available_moves(board))
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 2
            #print(board_cpy)
            value, mov = minimax(board_cpy, depth-1, "1", depth_initial, alpha, beta)
            
            if best_val > value:
                best_mov = move

            best_val = min(value, best_val)
            beta = min(beta, best_val)

            if alpha >= beta:
                break
            
        return best_val, best_mov
    
    else:
        best_val = -inf
        best_mov = None
        for move in get_available_moves(board, player):
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 1
            #print(board_cpy)
            value, mov = minimax(board_cpy, depth-1, "2", depth_initial, alpha, beta)
            if best_val < value:
                best_mov = move

            best_val = max(value, best_val)
            alpha = max(alpha, best_val)

            if alpha >= beta:
                break
        return best_val, best_mov

def can_remove(board, player):
        removals = []
        l = []

        #test vertical
        
        #test upward
        s = ""
        for line in range(max(last_line-3,1), last_line+1):
          
            state = board[last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(last_column,last_line-1),(last_column,last_line-2)])

        #test downward
        s = ""
        for line in range(last_line,  min(last_line+3,len(board[last_column-1]))+1):
        
            state = board[last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(last_column,last_line+1),(last_column,last_line+2)])
                 

        # test upward diagonals
        diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]

        col = last_column
        line =last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(board, column, line)[1]
            if coords == None:
                break

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            print(coords)
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            print(s)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(board, column, line)[5]
            if coords == None:
                break

        # test downward diagonals
        diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(board, column, line)[2]
            if coords == None:
                break

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            print(coords)
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            print(s)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(board, column, line)[4]
            if coords == None:
                break

        if len(removals) > 0:
            removals = [item for sublist in removals for item in sublist]
            return removals
        else:
            return None

if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
    

while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())
    last_column = 0
    last_line = 0
    

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        time.sleep(1)
        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        #Pega o tabuleiro completo
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        board = eval(resp.read()) #lista com 11 listas representando cada fileira na vertical (0 vazio, 1 player 1 e 2 player 2)

        # Escolhe um movimento aleatoriamente
        #movimento = random.choice(movimentos)        

        movimento = minimax(board, len(movimentos), str(player), len(movimentos))
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        msg = eval(resp.read())
        #print("mensagem" + strmsg)

        if msg[0] == 2:
            print("sanduiche")
            resp = urllib.request.urlopen("%s/tabuleiro" % host)
            board = eval(resp.read())
            movimento = can_remove(board, player)
            print(movimento)
            resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
            msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
    
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)


