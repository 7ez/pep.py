from reader import PacketReader

# Heartbeat + login_reply + notification.
packet = b'\x08\x00\x00\x00\x00\x00\x00\x05\x00\x00\x04\x00\x00\x00\xe8\x03\x00\x00\x18\x00\x00\x0f\x00\x00\x00\x0b\rHello, world!Y\x00\x00\x00\x00\x00\x00'

def read_packet():
    reader = PacketReader(packet, len(packet))
    
    # Read Ping
    print(reader.read_uint16())
    reader.skip(1)
    print(reader.read_uint32())
    
    # Read Login Reply
    print(reader.read_uint16())
    reader.skip(1)
    print(reader.read_uint32())
    print(reader.read_int32())
    
    # Read notification.
    print(reader.read_uint16())
    reader.skip(1)
    print(reader.read_uint32())
    print(reader.read_string_py())
    
def read_packet_np():
    reader = PacketReader(packet, len(packet))
    
    # Read Ping
    reader.read_uint16()
    reader.skip(1)
    reader.read_uint32()
    
    # Read Login Reply
    reader.read_uint16()
    reader.skip(1)
    reader.read_uint32()
    reader.read_int32()
    
    # Read notification.
    reader.read_uint16()
    reader.skip(1)
    reader.read_uint32()
    reader.read_string_py()

read_packet()   
while True:
    read_packet_np()
