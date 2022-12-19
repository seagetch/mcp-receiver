#from mcp_receiver.receiver  import Receiver
from mcp_receiver.vmcsender import VMCSender
from mcp_receiver.dummyreceiver  import DummyReceiver
#from mcp_receiver.dumper import ScreenDumper
import socket
import queue

from mcp_receiver.runner import Runner

class DumpServer(Runner):
    def __init__(self, addr = "localhost", port=39539):
        self.addr = addr
        self.port = port

    def loop(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.addr, self.port))
        while True:
            try:
                message, client_addr = self.socket.recvfrom(2048)
                print("Got:", message)
            except KeyError as e:
                print(e)



q = queue.Queue()
#recv = Receiver()
send = VMCSender()
recv = DummyReceiver()
#send = ScreenDumper()
watcher = DumpServer(port=39539)

watcher.run(q)
recv.run(q)
send.run(q)