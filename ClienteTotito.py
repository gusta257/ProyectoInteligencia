# BIBLIOTECAS NECESARIAS

import socketio
import random

# ESTABLECIENDO QUE ES CLIENTE
sio = socketio.Client()

# CLASE CON DATOS DE LA PARTIDA
class Juego:
    def __init__(self):
        self.turno = 0
        self.enemy_turn_id = 0
        self.user_name = ""
        self.tournament_id = ""
        self.gameFinished = False
        self.game_id = 0
        self.player_turn_id = 0
        self.winner_turn_id = 0

# CONEXION AL SERVER
@sio.on('connect')
def connect():
    # Client has connected
    print("Conectado: " + juego.user_name);
    # Signing signal
    sio.emit('signin', {
        'user_name': juego.user_name,
        'tournament_id': juego.tournament_id,  
        'user_role': "player"
    })

# LANZAMIENTO DEL TIRO
@sio.on('ready')
def on_ready(data):
    juego.gameFinished = False
    juego.game_id = data['game_id']
    if(data['player_turn_id'] == 1):
        juego.player_turn_id = data['player_turn_id']
        juego.enemy_turn_id = 2
    else:
        juego.player_turn_id = data['player_turn_id']
        juego.enemy_turn_id = 1
	
    movement = tiro(data['board'],juego.player_turn_id)
    
    print("Tiro: " + str(movement[0]) + ", " + str(movement[1]))

    sio.emit('play', {
        'tournament_id': juego.tournament_id,
        'player_turn_id': juego.player_turn_id,
        'game_id': juego.game_id,
        'movement': [movement[0],movement[1]]
    })

# FINALIZACION DEL JUEGO
@sio.on('finish')
def on_finish(data):
    juego.game_id = data['game_id']
    juego.winner_turn_id = data['winner_turn_id']
    
    if data['player_turn_id'] == data['winner_turn_id']:
        print("Eres el ganador")
    else:
        print("Perdiste")
    print('Juego Terminado!')
    juego.gameFinished = True

    sio.emit('player_ready', {
        'tournament_id': juego.tournament_id,
        'game_id': juego.game_id,
        'player_turn_id': juego.player_turn_id
    })

# MINIMAX BASADO EN https://www.youtube.com/watch?v=l-hh51ncgDI
# Y DE https://www.youtube.com/watch?v=trKjYdBASyQ
def minimax(board, move, depth, player_turn_id, alpha, beta, maximizingPlayer):

    if maximizingPlayer:
        idPlayerPlaying = juego.player_turn_id
    else:
        idPlayerPlaying = juego.enemy_turn_id
    
    puntos = heuristica(board, move, not maximizingPlayer)

    if depth == 0 or puntos != 0:
        return heuristica(board, move, not maximizingPlayer)

    if maximizingPlayer:
        maxEval = -1000000
        for i in range(len(board)):
            for j in range(len(board[0])):
                if int(board[i][j]) == 99:
                        value = minimax(board, (i,j), depth - 1, idPlayerPlaying, alpha, beta, False)
                        maxEval = max(maxEval, value)
                        alpha = max(alpha, value)
                        if beta <= alpha:
                                break
        board[move[0]][move[1]] = 99
        return maxEval

    else:
        minEval = 1000000
        for i in range(len(board)):
            for j in range(len(board[0])):
                if int(board[i][j]) == 99:
                        value = minimax(board, (i,j), depth - 1, idPlayerPlaying, alpha, beta, True)
                        minEval = min(minEval, value)
                        beta = min(beta, value)

        board[move[0]][move[1]] = 99
        return minEval


# TIRO A REALIZAR BASADO EN MINIMAX
def tiro(board, player_turn_id):
    bestScore = -1000000
    
    possibleMoves = []
   
    for i in range(len(board)):
        for j in range(len(board[0])):
            if int(board[i][j]) == 99:
                score = minimax(board, (i,j), 2, int(player_turn_id), -1000000, 1000000,False)
                if score > bestScore:
                        bestScore = score
                        possibleMoves.clear()
                if score >= bestScore:
                        possibleMoves.append((i,j))
    return possibleMoves[-1]
   
# HEURISTICA BASADA EN LA CANTIDAD DE PUNTOS DE CUADROS CERRADOS
# BASADO EN EL FORO DE CANVAS "COMO CONTAR PUNTOS"
def heuristica(oldBoard, move, maximizingPlayer):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    board = list(map(list, oldBoard))

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0
    # PUNTOS ANTES DE LA JUGADA
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    # JUGADA
    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0
    # PUNTOS LUEGO DE LA JUGADA
    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    # PUNTOS ASIGNADOS A LA JUGADA
    puntos = punteoFinal - punteoInicial
    if maximizingPlayer:
        return puntos
    else:
        return -puntos

#sio.connect('http://3.12.129.126:4000')
#sio.connect('http://localhost:4000')

juego = Juego()
juego.user_name = input("Ingrese su usuario: ")
juego.tournament_id = int(input("Ingrese el Tournament ID: "))
host = input("Ingrese el host: ")
#sio.connect('http://3.17.150.215:9000')
#sio.connect('http://localhost:4000')
sio.connect(host)

