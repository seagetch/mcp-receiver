import socket
import struct
from mcp_receiver.runner import Runner

data_keys = [b"#", b"head", b"ftyp", b"vrsn", b"sndf", b"ipad", b"rcvp", b"fram", b"fnum", b"time", b"btrs", b"btdt", b"btdt", b"bnid", b"tran"]

def _deserialize(data, index, length, is_list = False):
    result = [] if is_list else {}
    end_pos = index + length
    while end_pos - index > 8 and data[index+4:index+8] in data_keys:
        size = struct.unpack("@i", data[index: index+4])[0]
        index += 4
        field = data[index:index+4]
        index += 4
        value, index = _deserialize(data, index, size, field == b"btrs")
        if is_list:
            result.append(value)
        else:
            result[field.decode()] = value
    if len(result) == 0:
        body  = data[index:index+length]
        return body, index + len(body)
    else:
        return result, index

def _process_packet(packet):
    data = _deserialize(packet, 0, len(packet))[0]
    data["head"]["ftyp"] = data["head"]["ftyp"].decode()
    data["head"]["vrsn"] = ord(data["head"]["vrsn"])
    data["sndf"]["ipad"] = struct.unpack("@II", data["sndf"]["ipad"])
    data["sndf"]["rcvp"] = struct.unpack("@H", data["sndf"]["rcvp"])[0]
    data["fram"]["fnum"] = struct.unpack("@I", data["fram"]["fnum"])[0]
    data["fram"]["time"] = struct.unpack("@I", data["fram"]["time"])[0]
    for item in data["fram"]["btrs"]:
        item["bnid"] = struct.unpack("@H", item["bnid"])[0]
        item["tran"] = struct.unpack("@fffffff", item["tran"])
    return data


class Receiver(Runner):
    def __init__(self, addr = "localhost", port = 12351):
        self.addr = addr
        self.port = port

    def loop(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.addr, self.port))
        while True:
            message, client_addr = self.socket.recvfrom(2048)
            data = _process_packet(message)
            self.queue.put(data)
