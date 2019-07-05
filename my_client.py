import urllib.request
import sys
import random
import time
from math import inf
import copy

#first_move = ()
sanduiche = None
ant_movimentos_disp = 80

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

def heuristic1(board, player):

    cont = 0
    seq = 0
    
    for col in range(0, len(board)):
        s = ""
        for line in range(len(board[col])):
            state = board[col][line]
            #s += str(state)

            if state == 0:
                cont = cont +1
            elif state == player:
                seq = seq + 1
            else:
                cont = 0

            if cont + seq == 5:
                return +15*seq

    return -5

def heuristic2(board, player):

    # test upward diagonals

    cont = 0
    seq = 0
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            #s += str(state)

            if state == 0:
                cont = cont +1
            elif state == player:
                seq = seq + 1
            else:
                cont = 0

            if cont + seq == 5:
                return +10*seq
           
            coords = neighbors(board, column, line)[1]

    return -5

def heuristic3(board, player):

    cont = 0
    seq = 0
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

            if state == 0:
                cont = cont +1
            elif state == player:
                seq = seq + 1
            else:
                cont = 0

            if cont + seq == 5:
                return +10*seq           

            coords = neighbors(board, column, line)[4]

    return -5         


def minimax(board, depth, player, depth_initial, alpha=-inf, beta=inf):
    """ 
    Minimax algorithm that choose the best movement in board
    Args:
        board (list): the state of the board
        depth (int): how many free position the board has
        player (str): player ("X" or "O") 
    Returns:
        tuple: score and best move
    """
    global sanduiche

    h = heuristic1(board, player) + heuristic2(board, player) + heuristic3(board, player)
    #h = h + heuristic2(board, player)

    final_state = is_final_state(board)
    if final_state is not None:
        if final_state == 1:
            return -100 - depth, board
        else:
            return 100 + depth, board
    if depth == depth_initial-2:
        return h, board 

    
    moves = get_available_moves(board, player)
    #print("moves " +  str(len(moves)))
    
    #p_list = [(1,0),(2,0),(2,1),(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(5,4),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(8,0),(8,1),(9,0),(0,0),(0,1),(0,2),(0,3),(0,4),(1,1),(1,2),(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4),(1,5),(2,5),(2,6),(3,5),(3,6),(3,7),(4,5),(4,6),(4,7),(4,8),(8,5),(8,6),(9,5),(6,4),(7,3),(8,2),(8,3),(8,4),(9,1),(9,2),(9,3),(9,4),(10,0),(10,1),(10,2),(10,3),(10,4)]
    #p_list = [(6,5), (6,6), (6,7), (6,8), (6,9), (6,10), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9), (5,5), (5,6), (5,7), (5,8), (5,9), (8,4), (8,5), (8,6), (8,7), (8,8), (4,5), (4,6), (4,7), (4,8), (6,3), (6,2), (6,1), (7,3), (7,2), (7,1), (5,4), (5,3), (5,2), (5,1), (8,3), (8,2), (8,1), (4,4), (4,3), (4,2), (4,1), (9,4), (9,5), (9,6), (9,7), (3,4), (3,5), (3, 6), (3,7), (9,3), (9,2), (9,1), (3,3), (3,2), (3,1), (10,3), (10,4), (10,5), (10,6), (2,4), (2,5), (2,6), (10,2), (10,1), (2,3), (2,2), (2,1), (11,3), (11,4), (11,5), (1,3), (1,4), (1,5), (11,2), (11,1), (1,2), (1,1)]

    #p_list = p_list.reverse()
    #for item in p_list:
        #if item in moves:
           # moves.remove(item)
           #moves.append(item)

    if sanduiche != None:
    	print(moves)
    	moves.remove((sanduiche[0],sanduiche[1]))
    	sanduiche = None

    #print(moves)

    if player == "2":
        best_val = inf
        best_mov = None
        for move in moves:
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
        for move in moves:
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

def can_remove(board, player, last_column, last_line):
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
num_movimentos = 0
while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())
    last_column = 0
    last_line = 0 
    #sanduiche = None   

    movimentos_iniciais = [(5,4), (6,6), (6,5), (7,4)]
    

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
        resp = urllib.request.urlopen("%s/num_movimentos" % host)

        #last_num_movimentos += 2
        #last_num_movimentos = int(num_movimentos)
        num_movimentos = eval(resp.read())
        #print(num_movimentos)
        #print(last_num_movimentos)
        msg = ""

        #global sanduiche

        movimentos_disp = get_available_moves(board, player)
        print("moves " + str(len(movimentos_disp)))
        print(ant_movimentos_disp)
        print(len(movimentos_disp))

        #primeira jogada escolhe entre o miolho do meio do tabuleiro
        if num_movimentos < 2:
            movimento = random.choice(movimentos_iniciais)
            while movimento not in movimentos_disp:
            	movimento = random.choice(movimentos_iniciais)
            #first_move = movimento
            last_column = movimento[0]
            last_line = movimento[1]
            resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[0],movimento[1]))
            msg = eval(resp.read())
        else:
        	if ant_movimentos_disp - len(movimentos_disp) != 2:
        		#significa que ocorreu um sanduiche
	        	print("recebendo um sanduiche")
	        	resp = urllib.request.urlopen("%s/ultima_jogada" % host)
	        	sanduiche = eval(resp.read())	        	
	        	print(sanduiche)

        	movimento = minimax(board, len(movimentos), str(player), len(movimentos))
        	last_column = movimento[1][0]
        	last_line =  movimento[1][1]
        	resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        	msg = eval(resp.read())

        
        if msg[0] == 2:
            print("sanduiche")
            ant_movimentos_disp -=1
            resp = urllib.request.urlopen("%s/tabuleiro" % host)
            board = eval(resp.read())
            movimento = can_remove(board, player, last_column, last_line)
            resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
            msg = eval(resp.read())
        else:
        	ant_movimentos_disp = len(movimentos_disp)
       

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])

        #global last_num_movimentos
        
        #print(num_movimentos)
        #print(last_num_movimentos)
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)


