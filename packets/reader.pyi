# An interface file for the Cython reader.
class PacketReader:
    """A class for the reading of a packet buffer."""
    
    def __init__(self, packet_data: bytes, packet_length: int):
        ...
    
    def finished(self) -> bool:
        """Checks if the packet has been completely read."""
        ...
    
    def read_uint8(self) -> int: ...
    def read_uint16(self) -> int: ...
    def read_uint32(self) -> int: ...
    def read_uint64(self) -> int: ...
    def read_int8(self) -> int: ...
    def read_int16(self) -> int: ...
    def read_int32(self) -> int: ...
    def read_int64(self) -> int: ...
    def read_f32(self) -> float: ...
    
    def read_string_py(self) -> str:
        """Reads a uleb128 prefixed string from the packet."""
        ...
        
    def read_arr_py(self) -> list[int]:
        """Reads a u16 prefixed array of i32s from the packet."""
        ...
    
    def skip(self, length: int) -> None:
        """Skips `length` bytes of the buffer."""
