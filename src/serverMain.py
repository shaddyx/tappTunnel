import argparse
import logging

from tools import server_events

logging.basicConfig(level=logging.INFO)
logging.getLogger("engineio").setLevel(logging.WARNING)
import eventlet
import socketio

from server import ipResolver


parser = argparse.ArgumentParser(description='Virtual interface server')
parser.add_argument('port', type=int, help='server port')
args = parser.parse_args()


logging.info("Initializing socketio server")
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

clients = []

logging.info("adding listeners")
@sio.on(server_events.CONNECT)
def connect(sid, environ):
    logging.info("Client connected: {}".format(sid))
    clients.append(sid)
    sio.emit(server_events.IP, data = ipResolver.resolve(), room=sid)

@sio.on('data')
def message(sid, data):
    for client_sid in clients:
        if client_sid == sid:
            continue
        sio.emit(server_events.DATA, data=data, room=client_sid)

@sio.on(server_events.DISCONNECT)
def disconnect(sid):
    print('disconnect ', sid)
    clients.remove(sid)

logging.info("Starting listener")
listener = eventlet.listen(('0.0.0.0', args.port))
logging.info("Starting server")
eventlet.wsgi.server(listener, app)