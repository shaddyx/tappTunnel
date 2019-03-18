import argparse
import logging
import time

from event_bus import EventBus

from client import ws_client, events
from client.interface import Interface
from client.ws_client import WSClient

logging.basicConfig(level=logging.INFO)
logging.getLogger("engineio").setLevel(logging.WARNING)
parser = argparse.ArgumentParser(description='Virtual interface')
parser.add_argument('server', help='Server address ie: http://blabla.com:2323')
args = parser.parse_args()
bus = EventBus()

class Client:
    def __init__(self, bus: EventBus):
        self.client = WSClient()
        self.bus = bus
        self.interface = None

    def init(self):
        @self.bus.on(events.IP_RECEIVED)
        def ip(ip):
            self.interface = Interface(ip, self.bus)
            self.interface.run()

        @self.bus.on(events.SERVER_DATA)
        def data_drom_server(data):
            if self.interface:
                self.interface.sendPacket(data)

        @self.bus.on(events.DISCONNET)
        def disconnected():
            if self.interface:
                self.interface.close()


ws_client_instance = ws_client.WSClient
client = Client(bus)
client.init()
ws_client_instance.init()
while True:
    time.sleep(1)