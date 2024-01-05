import threading

class Runner:
    is_running = False

    def run(self, queue):
        self.queue = queue
        self.thread = threading.Thread(target=self.loop, args=())
        self.is_running = True
        self.thread.start()

    def close(self):
        self.is_running = False
        self.thread.join()