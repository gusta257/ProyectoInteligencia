import socketio

# standard Python
sio = socketio.Client()

class Juego:
    def __init__(self):
        self.user_name = ""
        self.tournament_id = ""
        self.user_role: 'player'


@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.on('connect')
def connect():
    # Client has connected
    print("Conectado: " + juego.user_name);
    # Signing signal
    sio.emit('signin', {
        'user_name': juego.user_name,
        'tournament_id': juego.tournament_id,  
        'user_role': juego.user_role
    })

'''
@sio.event
def connect():
    sio.emit('signin', {
    'user_name': 'Gustavo Adolfo De Leon Tobias',
    'tournament_id': 1000,
    'user_role': 'player'})
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('ok_signin')
def ok_signin():
    print('Successfully signed in!')

@sio.on('ready')
def ready(data):
    print('data of ready received', data)
   
@sio.on('finish')
def finish(data):
    print('tournament is over', data)
'''
#@sio.on('my message')
#def on_message(data):
#    print('I received a message!')
#@sio.on('my message')
#def on_message(data):
#    print('I received a message!')

#@sio.on('connect')
#def connect():
    # Client has connected
#    print("Conectado: " + vm.user_name);
    # Signing signal
#    sio.emit('signin', {
#        'user_name': vm.user_name,
#        'tournament_id': vm.tournament_id,  
#        'user_role': vm.user_role
#    })


 
#sio.connect('http://3.12.129.126:4000')
#sio.connect('http://localhost:4000')

juego = Juego()
juego.user_name = input("Ingrese su usuario: ")
juego.tournament_id = input("Ingrese el Tournament ID: ")
host = input("Ingrese el host: ")

sio.connect(host)







