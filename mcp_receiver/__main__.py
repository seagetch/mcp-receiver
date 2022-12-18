from .receiver  import Receiver
#from .vmcsender import VMCSender
from .dumper import ScreenDumper
import queue

q = queue.Queue()
recv = Receiver()
#send = VMCSender()
send = ScreenDumper()
recv.run(q)
send.run(q)