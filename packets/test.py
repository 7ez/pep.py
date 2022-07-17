from reader import PacketReader
import threading

packets = b"K\x00\x00\x04\x00\x00\x00\x13\x00\x00\x00"

def test():
    reader = PacketReader(packets, len(packets))

    reader.read_uint16()
    reader.read_uint8()
    reader.read_uint32()
    reader.read_int32()

def test_reader():
    while True:
        test()
        
for _ in range(6):
    threading.Thread(target=test_reader).start()
