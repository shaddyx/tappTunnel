import logging

from event_bus import EventBus
from tuntap import TunTap

from client import events
from tools import thread


class Interface:

    def __init__(self, ip, event_bus):
        self.tap = None
        self.ip = ip
        self.event_bus = event_bus  # type: EventBus

    @thread.run_in_thread
    def run(self):
        logging.info("Started loop")
        self.tap = TunTap(nic_type="Tap", nic_name="tap0")
        self.tap.config(ip=self.ip, mask="255.255.255.0")
        logging.debug("Device name: {} ip: {} mask: {}, max: {}".format(self.tap.name, self.tap.ip, self.tap.mask, self.tap.mac))
        while True:
            data = self.tap.read(90000)
            self.event_bus.emit(events.INTERFACE_DATA, data)

    def sendPacket(self, data):
        if self.tap:
            self.tap.write(data)
        else:
            logging.error("Ignoring packet: {}".format(data))

    def close(self):
        logging.info("closing tap interface...")
        if self.tap:
            self.tap.close()
        self.tap = None

