from pythonosc import udp_client, osc_bundle_builder, osc_message_builder
from mcp_receiver.runner import Runner

bone_map = [
    "Hips", #0
    "Spine", #2
    None, #1
    "Chest", #3
    None, #4
    "UpperChest", #5
    None, #6
    "-", #7
    "-", #8
    "Neck", #9
    "Head", #10
    "RightShoulder", #11
    "RightUpperArm", #12
    "RightLowerArm", #13
    "RightHand", #14
    "LeftShoulder", #15
    "LeftUpperArm", #16
    "LeftLowerArm", #17
    "LeftHand", #18
    "RightUpperLeg", #19
    "RightLowerLeg", #20
    "RightFoot", #21
    "RightToes", #22
    "LeftUpperLeg", #23
    "LeftLowerLeg", #24
    "LeftFoot", #25
    "LeftToes" #26
]

class VMCSender(Runner):
    def __init__(self, host = "localhost", port = 39540):
        self.host = host
        self.port = port

    def loop(self):
        client = udp_client.UDPClient(self.host, self.port)
        # Do some initialization here
        pass

        # Main loop
        while True:
            try:
                data = self.queue.get()
                if "skdf" in data:
                    msg_builder = osc_message_builder.OscMessageBuilder("/VMC/Ext/Root/Pos")
                    tran = data["skdf"]["bons"][0]["tran"]
                    msg_builder.add_arg("root")
                    msg_builder.add_arg(tran[4])
                    msg_builder.add_arg(tran[5])
                    msg_builder.add_arg(tran[6])
                    msg_builder.add_arg(tran[0])
                    msg_builder.add_arg(tran[1])
                    msg_builder.add_arg(tran[2])
                    msg_builder.add_arg(tran[3])
                    client.send(msg_builder.build())
                elif "fram" in data:
                    bdl_builder = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
                    skipped_pos = None
                    skipped_rot = None
                    for btdt in data["fram"]["btrs"]:
                        if bone_map[btdt["bnid"]] == "-":
                            pass
                        if bone_map[btdt["bnid"]]:
                            msg_builder = osc_message_builder.OscMessageBuilder("/VMC/Ext/Bone/Pos")
                            tran = btdt["tran"]
                            if skipped_pos is not None and skipped_rot is not None:
                                tran = [
                                    tran[0] * skipped_rot[0],
                                    tran[1] * skipped_rot[1],
                                    tran[2] * skipped_rot[2],
                                    tran[3] * skipped_rot[3],
                                    tran[4] + skipped_pos[0],
                                    tran[5] + skipped_pos[1],
                                    tran[6] + skipped_pos[2]
                                ]
                            skipped_pos = None
                            skipped_rot = None
                            msg_builder.add_arg(bone_map[btdt["bnid"]])
                            msg_builder.add_arg(tran[4])
                            msg_builder.add_arg(tran[5])
                            msg_builder.add_arg(tran[6])
                            msg_builder.add_arg(tran[0])
                            msg_builder.add_arg(tran[1])
                            msg_builder.add_arg(tran[2])
                            msg_builder.add_arg(tran[3])
                            bdl_builder.add_content(msg_builder.build())
                        elif skipped_pos is None:
                            skipped_pos = [tran[4], tran[5], tran[6]]
                            skipped_rot = [tran[0], tran[1], tran[2], tran[3]]
                        else:
                            skipped_pos = [skipped_pos[0] + tran[4], skipped_pos[1] + tran[5], skipped_pos[2] + tran[6]]
                            skipped_rot = [skipped_rot[0] * tran[0], skipped_rot[1] * tran[1], skipped_rot[2] * tran[2], skipped_rot[3] * tran[3]]
                    client.send(bdl_builder.build())
            except KeyError as e:
                print(e)