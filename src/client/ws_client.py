import logging

import socketio
from event_bus import EventBus

from client import events
from tools import server_events
from tools.thread import run_in_thread


class WSClient:
    def __init__(self, server, bus: EventBus):
        logging.info("Instantiating websocket client")
        self.sio = socketio.Client()
        self.server = server
        self.bus = bus

    def init(self):
        logging.info("Initializing websocket client")

        @self.sio.on(server_events.CONNECT)
        def on_connect():
            logging.info("Connection established")
            self.bus.emit(events.CONNECT)

        @self.sio.on(server_events.IP)
        def on_message(ip):
            logging.info("Received ip: {}".format(ip))
            self.bus.emit(events.IP_RECEIVED, ip)

        @self.sio.on(server_events.DATA)
        def on_message(data):
            self.bus.emit(events.SERVER_DATA, data)

        @self.sio.on(server_events.DISCONNECT)
        def on_disconnect():
            self.bus.emit(events.DISCONNET)

    def send_data(self, data):
        self.sio.emit(server_events.DATA, data)

    @run_in_thread
    def connect(self):
        logging.info("Connecting to: {}".format(self.server))
        self.sio.connect(self.server)
        self.sio.wait()

    def request_ip(self):
        self.sio.emit(server_events.REQUEST_IP)

