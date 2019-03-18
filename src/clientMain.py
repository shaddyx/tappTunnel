import argparse
import logging
import time

from event_bus import EventBus

from client import ws_client, events
from client.interface import Interface

logging.basicConfig(level=logging.INFO)
logging.getLogger("engineio").setLevel(logging.WARNING)


parser = argparse.ArgumentParser(description='Virtual interface')
parser.add_argument('server', help='Server address ie: http://blabla.com:2323')
args = parser.parse_args()
bus = EventBus()

class Client:
    def __init__(self, ws_client: ws_client.WSClient, bus: EventBus):
        logging.info("Instantiating client")
        self.bus = bus
        self.interface = None
        self.ws_client = ws_client

    def init(self):
        logging.info("Initizlizing client")
        @self.bus.on(events.IP_RECEIVED)
        def ip(ip):
            if not self.interface:
                self.interface = Interface(ip, self.bus)
                self.interface.run()
            else:
                logging.error("Just reconnect...")

        @self.bus.on(events.SERVER_DATA)
        def data_drom_server(data):
            if self.interface:
                self.interface.sendPacket(data)

        @bus.on(events.INTERFACE_DATA)
        def packetFromTapReceived(data):
            self.ws_client.send_data(data)

        #@self.bus.on(events.DISCONNET)
        def disconnected():
            if self.interface:
                self.interface.close()

    def close(self):
        if self.interface:
            self.interface.close()
        self.interface = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

ws_client_instance = ws_client.WSClient(args.server, bus)
with Client(ws_client_instance, bus) as client:

    client.init()
    ws_client_instance.init()
    ws_client_instance.connect()
    ws_client_instance.request_ip()



    logging.info("Starting main loop")
    while True:
        time.sleep(1)

