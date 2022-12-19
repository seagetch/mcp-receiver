from pythonosc import udp_client, osc_bundle_builder, osc_message_builder
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
        client = udp_client.UDPClient(self.host, self.port)
        # Do some initialization here
        pass

        # Main loop
        while True:
            try:
                bdl_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
                data = self.queue.get()
                if "skdf" in data:
                    pass
                elif "fram" in data:
                    for btdt in data["fram"]["btrs"]:
                        if bone_map[btdt["bnid"]]:
                            msg_builder = osc_message_builder.OscMessageBuilder("/VMC/Ext/Bone/Pos")
                            tran = btdt["tran"]
                            msg_builder.add_arg(bone_map[btdt["bnid"]])
                            msg_builder.add_arg(tran[4])
                            msg_builder.add_arg(tran[5])
                            msg_builder.add_arg(tran[6])
                            msg_builder.add_arg(tran[0])
                            msg_builder.add_arg(tran[1])
                            msg_builder.add_arg(tran[2])
                            msg_builder.add_arg(tran[3])
                            bdl_builder.add_content(msg_builder.build())
                client.send(bdl_builder.build())
            except KeyError as e:
                print(e)