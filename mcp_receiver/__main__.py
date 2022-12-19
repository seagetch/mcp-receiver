from .receiver  import Receiver
from .vmcsender import VMCSender
import queue

q = queue.Queue()
recv = Receiver()
send = VMCSender()
recv.run(q)
send.run(q)