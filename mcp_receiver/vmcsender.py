import pythonosc
from mcp_receiver.runner import Runner


class VMCSender(Runner):
    def __init__(self, host = "localhost", port = 39539):
        self.host = host
        self.port = port

    def loop(self):
        client = pythonosc.udp_client.SimpleUDPClient(host, port)
        # Do some initialization here
        pass

        # Main loop
        while True:
            data = self.queue.get()
            for btdt in data["fram"]["btrs"]:
                client.send_message("/VMC/Ext/Bone/Pos", ["name"] + btdt["tran"])
