import logging

import socketio
from event_bus import EventBus

from client import events
from tools import server_events


class WSClient:
    def __init__(self, port, bus: EventBus):
        self.sio = socketio.Client()
        self.port = port
        self.bus = bus

    def init(self):
        @self.sio.on('connect')
        def on_connect():
            logging.info("Connection established")

        @events.bus.on(events.INTERFACE_DATA)
        def packetFromTapReceived(data):
            self.sio.emit(server_events.DATA, data)

        @self.sio.on(server_events.IP)
        def on_message(ip):
            logging.info("Received ip: {}".format(ip))
            self.bus.emit(events.IP_RECEIVED, ip)

        @self.sio.on(server_events.DATA)
        def on_message(data):
            self.bus.emit(events.SERVER_DATA, data)

        @self.sio.on('disconnect')
        def on_disconnect():
            self.bus.emit(events.DISCONNET)

    def connect(self):
        self.sio.connect(self, self.port)
        self.sio.wait()

