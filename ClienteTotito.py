import socketio
import random
# standard Python
sio = socketio.Client()

class Juego:
    def __init__(self):
        self.user_name = ""
        self.tournament_id = ""
        self.ready = False
        self.gameFinished = False
        self.game_id = 0
        self.player_turn_id = 0
        self.winner_turn_id = 0
        self.board = []
        #user_role: "player"

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
@sio.on('ready')
def on_ready(data):
    juego.gameFinished = False
    juego.game_id = data['game_id']
    juego.player_turn_id = data['player_turn_id']
    juego.board = data['board']
   
    juego.ready = True

    movement = []

    direction = random.randint(0, 1)
    position = random.randint(0, 29)

    while int(juego.board[direction][position]) != 99:
        direction = random.randint(0, 1)
        position = random.randint(0, 29)

    movement = [direction, position]
    print("Movement played: " + str(movement[0]) + ", " + str(movement[1]))

    sio.emit('play', {
        'tournament_id': juego.tournament_id,
        'player_turn_id': juego.player_turn_id,
        'game_id': juego.game_id,
        'movement': movement
    })
@sio.on('finish')
def on_finish(data):
    juego.game_id = data['game_id']
    juego.player_turn_id = data['player_turn_id']
    juego.winner_turn_id = data['winner_turn_id']
    if data['player_turn_id'] == data['winner_turn_id']:
        print("Eres el ganador")
    else:
        print("Perdiste")
    print('Game finished!')
    juego.gameFinished = True

    sio.emit('player_ready', {
        'tournament_id': juego.tournament_id,
        'game_id': juego.game_id,
        'player_turn_id': juego.player_turn_id
    })

#sio.connect('http://3.12.129.126:4000')
#sio.connect('http://localhost:4000')

juego = Juego()
juego.user_name = input("Ingrese su usuario: ")
juego.tournament_id = int(input("Ingrese el Tournament ID: "))
host = input("Ingrese el host: ")

sio.connect(host)







