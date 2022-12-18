from .receiver  import Receiver
#from .vmcsender import VMCSender
#from .dummyreceiver  import DummyReceiver
from .dumper import ScreenDumper
import queue

q = queue.Queue()
recv = Receiver()
#send = VMCSender()
#recv = DummyReceiver()
send = ScreenDumper()
recv.run(q)
send.run(q)