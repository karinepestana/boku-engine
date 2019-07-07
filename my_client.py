import urllib.request
import sys
import random
import time
from math import inf
import copy

sanduiche = None
ant_movimentos_disp = 80

#FUNÇÕES COPIADAS DO SERVIDOR

def get_available_moves(board, player):
    l = []

    for column in range(len(board)):
        for line in range(len(board[column])):
            if board[column][line] == 0:
                l.append((column + 1, line + 1))
    return l

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
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
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
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
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

#FUNÇÕES IMPLEMENTADAS

#Heuristicas que buscam encontrar possibilidades de fazer as jogadas
def h_line(board, player):

    cont = 0
    seq = 0

    for line in range(len(board)):
        state = board[line]
        if state == player or state == 0:
            if state == 0:
            	cont += 1
            else:
            	seq += 1
            if (cont + seq) == 5:
            	if seq == 0:
            		seq = 1
            	return +10*seq
        else:
        	cont = 0
        	seq = 0            

    return -1

def h_upward_diagonals(board, player):

    # test upward diagonals
    cont = 0
    seq = 0

    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            if state == player or state == 0:               
	            if state == 0:
	            	cont += 1
	            else:
	            	seq += 1
	            if (cont + seq) == 5:
	            	if seq == 0:
	            		seq = 1
	            	if column in [6, 5, 4, 7]:
	            		return +10*seq, True
	            	else:
	            		return +10*seq, False
            else:
	            cont = 0
	            seq = 0

            coords = neighbors(board, column, line)[1]

    return -1, False

def h_downward_diagonals(board, player):

	cont = 0
	seq = 0
	diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
	for column_0, line_0 in diags:
		coords = (column_0, line_0)
		while coords != None:
			column = coords[0]
			line = coords[1]
			state = board[column - 1][line - 1]
			if state == player or state == 0:
				if state == 0:
					cont += 1
				else:
					seq += 1
				if (cont + seq) == 5:
					if seq == 0:
						seq = 1
					if column in [6, 5, 4, 7]:
						return +10*seq, True
					else:
						return +10*seq, False
			else:
				cont = 0
				seq = 0
			coords = neighbors(board, column, line)[4]
	return -1, False

def h_line_sanduiche(board, player, enemy):

    s = ""
    for line in range(len(board)):
        state = board[line]
        s += str(state)

        if len(s) == 4:
        	#verificar sanduiche
        	if s == (str(player)+str(enemy)+str(enemy)+str("0")):
        		return +10
        	else:
        		s = ""           

    return -1

def h_upward_diagonals_sanduiche(board, player, enemy):

    # test upward diagonals
    s = ""

    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)

            if len(s) == 4:
            	if s == (str(player)+str(enemy)+str(enemy)+str("0")):
            		return +10
            	else:
            		s = ""            

            coords = neighbors(board, column, line)[1]

    return -1

def h_downward_diagonals_sanduiche(board, player, enemy):
	s = ""

	diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

	for column_0, line_0 in diags:
		coords = (column_0, line_0)
		while coords != None:
			column = coords[0]
			line = coords[1]
			state = board[column - 1][line - 1]
			s += str(state)

			if len(s) == 4:
				if s == (str(player)+str(enemy)+str(enemy)+str("0")):
					return +10
				else:
					s = ""
			
			coords = neighbors(board, column, line)[4]
	return -1

def heuristica_total(board, player):

	estado_final = is_final_state(board)
	if estado_final is not None:
		if estado_final == 1:
			return 1000
		else:
			return -1000

	h = 0  

	#pré calcula os valores
	h_upward_diagonals_p1, h_ud_p1 = h_upward_diagonals(board, 1)
	h_upward_diagonals_p2, h_ud_p2 = h_upward_diagonals(board, 2)

	h_downward_diagonals_p1, h_dd_p1 = h_downward_diagonals(board, 1) 
	h_downward_diagonals_p2, h_dd_p2 = h_downward_diagonals(board, 2)

	h_upward_diagonals_sand_p1 = h_upward_diagonals_sanduiche(board, 1, 2)
	h_upward_diagonals_sand_p2 = h_upward_diagonals_sanduiche(board, 2, 1)

	h_downward_diagonals_sand_p1 = h_downward_diagonals_sanduiche(board, 1, 2) 
	h_downward_diagonals_sand_p2 = h_downward_diagonals_sanduiche(board, 2, 1)


	for col in range(0, len(board)):
		h_line_p1 = h_line(board[col], 1) 
		h_line_p2 = h_line(board[col], 2)

		h_line_sand_p1 = h_line_sanduiche(board[col], 1, 2) 
		h_line_sand_p2 = h_line_sanduiche(board[col], 2, 1)

		if player == 1:
			#testando as verticais
			if h_line_p2 != -1:
				h -= 20
				if h_line_p2 > 30:
					h-=30
				h -= h_line_p2
			if h_line_p1 != -1:
				h += 30
			else:
				h -= 20
			if h_line_sand_p1 != -1:
				h += h_line_sand_p1
			if col in [5,6,7]:
				h += 100

		if player == 2:
		#testando as verticais
			if h_line_p1 != -1:
				h += 20
				if h_line_p1 > 30:
					h+=60
				h += h_line_p2
			if h_line_p2 != -1:
				h -= 30
			else:
				h += 20
			if h_line_sand_p2 != -1:
				h -= h_line_sand_p2
			if col in [5,6,7]:
				h-= 100

	if player == 1:
		#testando as diagonais superiores
		if h_upward_diagonals_p2 != -1:
			h -= 50
			if h_upward_diagonals_p2 > 30:
				h-=30
			h -= h_upward_diagonals_p2
		if h_upward_diagonals_p1 != -1:
			h += 30
		else:
			h -= 20
		if h_upward_diagonals_sand_p1 != -1:
			h += h_upward_diagonals_sand_p1
		if h_ud_p1:
			h+= 100

		#testando as diagonais inferiores
		if h_downward_diagonals_p2 != -1:
			h -= 50
			if h_downward_diagonals_p2 > 30:
				h-=30
			h -= h_downward_diagonals_p2
		if h_downward_diagonals_p1 != -1:
			h += 30
		else:
			h -= 20
		if h_upward_diagonals_sand_p2 != -1:
			h += h_upward_diagonals_sand_p2
		if h_dd_p1:
			h+= 100

	if player == 2:
		#testando as diagonais superiores
		if h_upward_diagonals_p1 != -1:
			h += 50
			if h_upward_diagonals_p1 > 30:
				h+=60
			h += h_upward_diagonals_p1
		if h_upward_diagonals_p2 != -1:
			h -= 20
		else:
			h += 30
		if h_upward_diagonals_sand_p1 != -1:
			h -= h_upward_diagonals_sand_p1
		if h_dd_p2:
			h-= 100

		#testando as diagonais inferiores
		if h_downward_diagonals_p1 != -1:
			h += 50
			if h_downward_diagonals_p1 > 30:
				h+=60
			h += h_downward_diagonals_p1
		if h_downward_diagonals_p2 != -1:
			h -= 20
		else:
			h += 30
		if h_downward_diagonals_p2 != -1:
			h -= h+h_downward_diagonals_p2
		if h_dd_p2:
			h-= 100

	return h

def minimax(board, depth, player, depth_initial, alpha=-inf, beta=inf):

    global sanduiche
    
    moves = get_available_moves(board, player)

    if depth == depth_initial-2:
    	h = heuristica_total(board, player)
    	return h, (-1, -1)

    if sanduiche != None:
    	if ((sanduiche[0],sanduiche[1])) in moves:
    		moves.remove((sanduiche[0],sanduiche[1]))
    	sanduiche = None

    if player == 2:
        best_val = inf
        best_mov = None
        for move in moves:         
            board_cpy = copy.deepcopy(board)
            column, line = move
            board_cpy[column-1][line-1] = 2
            value, mov = minimax(board_cpy, depth-1, 1, depth_initial, alpha, beta)
            
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
            value, mov = minimax(board_cpy, depth-1, 2, depth_initial, alpha, beta)
            if best_val < value:
                best_mov = move

            best_val = max(value, best_val)
            alpha = max(alpha, best_val)

            if alpha >= beta:
                break
        return best_val, best_mov


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
        num_movimentos = eval(resp.read())

        msg = ""
        movimentos_disp = get_available_moves(board, player)

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
	        	print("Recebeu um sanduiche")
	        	resp = urllib.request.urlopen("%s/ultima_jogada" % host)
	        	sanduiche = eval(resp.read())	        	
	        	print("Posição removida: " + str(sanduiche))

        	movimento = minimax(board, len(movimentos), str(player), len(movimentos))
        	last_column = movimento[1][0]
        	last_line =  movimento[1][1]
        	resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        	msg = eval(resp.read())

        
        if msg[0] == 2:
            print("Faz um sanduiche")
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


    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)


