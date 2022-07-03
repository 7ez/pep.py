from reader import PacketReader

packets = b"K\x00\x00\x04\x00\x00\x00\x13\x00\x00\x00"

reader = PacketReader(packets, len(packets))

print(reader.read_uint16())
print(reader.read_uint8())
print(reader.read_uint32())
print(reader.read_int32())
