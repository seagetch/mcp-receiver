import socket
import struct
from mcp_receiver.runner import Runner

def is_field(name):
    return name.isalpha()

def _deserialize(data, index, length, is_list = False):
    result = [] if is_list else {}
    end_pos = index + length
    while end_pos - index > 8 and is_field(data[index+4:index+8]):
        size = struct.unpack("@i", data[index: index+4])[0]
        index += 4
        field = data[index:index+4]
        index += 4
        value, index2 = _deserialize(data, index, size, field in [b"btrs", b"bons"])
        index = index2
        if is_list:
            result.append(value)
        else:
            result[field.decode()] = value
    if len(result) == 0:
        body  = data[index:index+length]
        return body, index + len(body)
    else:
        return result, index

def _process_packet(message):
    data = _deserialize(message, 0, len(message), False)[0]
    data["head"]["ftyp"] = data["head"]["ftyp"].decode()
    data["head"]["vrsn"] = ord(data["head"]["vrsn"])
    data["sndf"]["ipad"] = struct.unpack("@BBBBBBBB", data["sndf"]["ipad"])
    data["sndf"]["rcvp"] = struct.unpack("@H", data["sndf"]["rcvp"])[0]
    if "skdf" in data:
        for item in data["skdf"]["bons"]:
            item["bnid"] = struct.unpack("@H", item["bnid"])[0]
            item["pbid"] = struct.unpack("@H", item["pbid"])[0]
            item["tran"] = struct.unpack("@fffffff", item["tran"])
    elif "fram" in data:
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
            try:
                message, client_addr = self.socket.recvfrom(2048)
                data = _process_packet(message)
                self.queue.put(data)
            except KeyError as e:
                print(e)
