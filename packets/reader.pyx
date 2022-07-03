from libc.stdint cimport *
from libc.stdlib cimport malloc, free

cdef extern from "<stdlib.h>" nogil:
    void *memcpy(void *dest, void *src, size_t n)

cdef const char* EMPTY_STR = ""

cdef class PacketReader:
    """A class made for reading a packet buffer."""

    cdef char* buffer
    cdef char* end

    def __init__(self, bytes packet_data, size_t buffer_size):
        self.buffer = <char*>packet_data
        self.end = self.buffer + buffer_size

    cpdef bint finished(self):
        """Checks if the buffer has been fully read."""

        return self.buffer >= self.end

    cpdef uint8_t read_uint8(self):
        cdef uint8_t val = <uint8_t>self.buffer[0]
        self.buffer += 1
        return val

    cpdef uint16_t read_uint16(self):
        cdef uint16_t val
        memcpy(&val, self.buffer, 2)
        self.buffer += 2
        return val

    cpdef uint32_t read_uint32(self):
        cdef uint32_t val
        memcpy(&val, self.buffer, 4)
        self.buffer += 4
        return val
    
    cpdef uint64_t read_uint64(self):
        cdef uint64_t val
        memcpy(&val, self.buffer, 8)
        self.buffer += 8
        return val
    
    cpdef float read_f32(self):
        cdef float val
        memcpy(&val, self.buffer, 2)
        self.buffer += 2
        return val

    cpdef int8_t read_int8(self):
        cdef int8_t val = <int8_t>self.buffer[0]
        self.buffer += 1
        return val
    
    cpdef int16_t read_int16(self):
        cdef int16_t val
        memcpy(&val, self.buffer, 2)
        self.buffer += 2
        return val
    
    cpdef int32_t read_int32(self):
        cdef int32_t val
        memcpy(&val, self.buffer, 4)
        self.buffer += 4
        return val

    cpdef int64_t read_int64(self):
        cdef int64_t val
        memcpy(&val, self.buffer, 8)
        self.buffer += 8
        return val

    # In theory this should be higher, but osu doesnt allow strings
    # over 2048 chars.
    cpdef uint16_t read_uleb128(self):
        cdef uint16_t val = 0
        cdef uint16_t shift = 0
        cdef int8_t byte = 0
        while True:
            byte = self.buffer[0]
            self.buffer += 1
            val |= (byte & 0x7f) << shift
            if (byte & 0x80) == 0:
                break
            shift += 7
        return val
    
    cdef char* read_string(self):
        cdef uint8_t exists = self.read_uint8()

        if exists != 0xb:
            return EMPTY_STR
        
        cdef uint16_t length = self.read_uleb128()

        # Don't allow someone to segfault by sending an incorrect length.
        if length > self.end - self.buffer:
            return EMPTY_STR

        # TODO: Check if python garbage collects this properly.
        cdef char *str = <char*>malloc(length + 1)
        memcpy(str, self.buffer, length)
        str[length] = "\0"
        self.buffer += length
        return str
    
    cpdef str read_string_py(self):
        cdef char* string = self.read_string()
        cdef str py_string = string.decode("utf-8")
        free(string)
        return py_string

    cpdef skip(self, size_t length):
        self.buffer += length
