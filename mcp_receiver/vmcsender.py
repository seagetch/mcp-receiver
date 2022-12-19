from pythonosc import udp_client
from mcp_receiver.runner import Runner

bone_map = [
    "Hips", #0
    None, #1
    "Spine", #2
    None, #3
    "Chest", #4
    None, #5
    "UpperChest", #6
    None, #7
    "Neck", #8
    None, #9
    "Head", #10
    "LeftShoulder", #11
    "LeftUpperArm", #12
    "LeftLowerArm", #13
    "LeftHand", #14
    "RightShoulder", #15
    "RightUpperArm", #16
    "RightLowerArm", #17
    "RightHand", #18
    "LeftUpperLeg", #19
    "LeftLowerLeg", #20
    "LeftFoot", #21
    "LeftToes", #22
    "RightUpperLeg", #23
    "RightLowerLeg", #24
    "RightFoot", #25
    "RightToes" #26
]

class VMCSender(Runner):
    def __init__(self, host = "localhost", port = 39539):
        self.host = host
        self.port = port

    def loop(self):
        client = udp_client.SimpleUDPClient(self.host, self.port)
        # Do some initialization here
        pass

        # Main loop
        while True:
            try:
                data = self.queue.get()
                if "skdf" in data:
                    pass
                elif "fram" in data:
                    for btdt in data["fram"]["btrs"]:
                        if bone_map[btdt["bnid"]]:
                            tran = btdt["tran"]
                            client.send_message("/VMC/Ext/Bone/Pos", [bone_map[btdt["bnid"]], tran[4], tran[5], tran[6], tran[0], tran[1], tran[2], tran[3]])
            except KeyError as e:
                print(e)