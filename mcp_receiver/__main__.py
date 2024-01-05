from .receiver  import Receiver
from .vmcsender import VMCSender
import queue
import time
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--unix-support", action='store_true', help='Enable support for UNIX timestamp in mocopi input format')
    args = parser.parse_args()

    q = queue.Queue()
    recv = Receiver(unix_support=args.unix_support)
    send = VMCSender()

    try:
        recv.run(q)
        send.run(q)
        time.sleep(3600)
    except KeyboardInterrupt:
        pass

    recv.close()
    send.close()
