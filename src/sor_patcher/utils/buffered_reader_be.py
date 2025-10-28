import io
import struct

from io import BufferedReader, RawIOBase
from typing import Optional

from .padding import pad


class BufferedReaderBE:
    reader: Optional[BufferedReader] = None

    def __init__(self, f: RawIOBase | io.BytesIO) -> None:
        self.reader = BufferedReader(f)

    def read(self, bytes_count: int) -> bytes:
        if self.reader is None:
            raise IOError(f'Stream was closed!')
        return self.reader.read(bytes_count)

    def read_boolean(self) -> bool:
        return self.read_u8() > 0

    def read_s8(self) -> int:
        return struct.unpack('b', self.read(1))[0]

    def read_s16(self) -> int:
        return struct.unpack('>h', self.read(2))[0]

    def read_s24(self) -> int:
        return struct.unpack('>i', b'\x00' + self.read(3))[0]

    def read_s32(self) -> int:
        return struct.unpack('>i', self.read(4))[0]

    def read_s64(self) -> int:
        return struct.unpack('>q', self.read(8))[0]

    def read_u8(self) -> int:
        return struct.unpack('B', self.read(1))[0]

    def read_u16(self) -> int:
        return struct.unpack('>H', self.read(2))[0]

    def read_u24(self) -> int:
        return struct.unpack('>I', b'\x00' + self.read(3))[0]

    def read_u32(self) -> int:
        return struct.unpack('>I', self.read(4))[0]

    def read_u64(self) -> int:
        return struct.unpack('>Q', self.read(8))[0]

    def read_f32(self) -> int:
        return struct.unpack('>f', self.read(4))[0]

    def read_f64(self) -> int:
        return struct.unpack('>d', self.read(8))[0]

    def read_string(self, length: Optional[int] = None) -> str:
        if length is not None:
            return self.read(length).decode('utf-8')

        ret = ''
        while True:
            c = self.read_u8()
            if c == 0:
                break
            ret += chr(c)

        return ret

    def read_wstring(self, length: Optional[int] = None) -> str:
        if length is not None:
            return self.read(length).decode('utf-16be')

        ret = ''
        while True:
            c = self.read_u16()
            if c == 0:
                break
            ret += chr(c)

        return ret

    def align_to(self, bits_count: int) -> None:
        self.seek(pad(self.tell(), bits_count), 1)

    def tell(self) -> int:
        if self.reader is None:
            raise IOError(f'Stream was closed!')
        return self.reader.tell()

    def seek(self, off: int, origin: int) -> None:
        if self.reader is None:
            raise IOError(f'Stream was closed!')
        self.reader.seek(off, origin)

    def close(self) -> None:
        if self.reader is None:
            raise IOError(f'Stream was closed!')
        self.reader.close()
