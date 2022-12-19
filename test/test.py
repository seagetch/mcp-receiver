from mcp_receiver.receiver  import Receiver
from mcp_receiver.vmcsender import VMCSender
from mcp_receiver.dummyreceiver  import DummyReceiver
#from mcp_receiver.dumper import ScreenDumper
import socket
import queue
import glob
import os.path

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
                print("Got [%d]:"%len(message), message)
            except KeyError as e:
                print(e)

class DummyBVHSender(Runner):
    def __init__(self, addr = "localhost", port=12351):
        self.addr = addr
        self.port = port

    def loop(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        payloads = []
        for fn in sorted(glob.glob("test/stuff/*")):
            with open(fn, "rb") as f:
                payloads.append(f.read())
        self.socket.sendto(payloads[0], (self.addr, self.port))
        index = 1
        while True:
            try:
                if index == len(payloads):
                    index = 1
                self.socket.sendto(payloads[index], (self.addr, self.port))
                index += 1
            except KeyError as e:
                print(e)


q = queue.Queue()
send = VMCSender()
#recv = DummyReceiver()
#send = ScreenDumper()
watcher = DumpServer(port=39539)
if os.path.exists("test/stuff"):
    recv = Receiver()
    bvh = DummyBVHSender()
else:
    recv = DummyReceiver()
    bvh = None

watcher.run(q)
send.run(q)
recv.run(q)
if bvh:
    bvh.run(q)