from .receiver  import Receiver
from .vmcsender import VMCSender
import queue
import time


if __name__ == '__main__':
    q = queue.Queue()
    recv = Receiver()
    send = VMCSender()

    try:
        recv.run(q)
        send.run(q)
        time.sleep(3600)
    except KeyboardInterrupt:
        pass

    recv.close()
    send.close()
