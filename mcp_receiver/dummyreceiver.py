import time
from mcp_receiver.runner import Runner

class DummyReceiver(Runner):
    def __init__(self):
        pass

    def loop(self):

        # Main loop
        id = 0
        while True:
            data = {
                "head": { "ftyp": "dummy", "vrsn": 0},
                "sndf": { "ipad": (0, 1), "rcvp": 12351},
                "fram": { "fnum": id, "time": int(1000*time.time()), 
                    "btrs": [{
                        "bnid": i,
                        "tran": (0, 0, 0, 0, 0, 0, 0)} for i in range(0, 27)]}}
            data = self.queue.put(data)
            print(data)
            time.sleep(1)
