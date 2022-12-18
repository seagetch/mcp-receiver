import threading

class Runner:
    def run(self, queue):
        self.queue = queue
        self.thread = threading.Thread(target=self.loop, args=())
        self.thread.start()