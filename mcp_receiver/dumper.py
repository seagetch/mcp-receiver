from mcp_receiver.runner import Runner


class ScreenDumper(Runner):
    def __init__(self):
        pass

    def loop(self):

        # Main loop
        while True:
            data = self.queue.get()
            print(data)