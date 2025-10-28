import io
import math
import struct

from io import BufferedWriter, RawIOBase
from typing import Optional

from ..utils.padding import pad

BUF_SIZE = 8192


class BufferedWriterBE:
    writer: Optional[BufferedWriter] = None

    def __init__(self, f: RawIOBase | io.BytesIO) -> None:
        self.writer = BufferedWriter(f)

    def write(self, datas: bytes) -> None:
        if self.writer is None:
            raise IOError(f'Stream was closed!')
        iter_count = math.ceil(len(datas) / BUF_SIZE)
        for i in range(iter_count):
            beg = i * BUF_SIZE
            end = (i + 1) * BUF_SIZE if len(datas) - beg >= BUF_SIZE else beg + (len(datas) - beg)
            self.writer.write(datas[beg:end])
            self.writer.flush()

    def write_boolean(self, value: bool) -> None:
        self.write_u8(1 if value else 0)

    def write_s8(self, value: int) -> None:
        self.write(struct.pack('b', value))

    def write_s16(self, value: int) -> None:
        self.write(struct.pack('>h', value))

    def write_s24(self, value: int) -> None:
        self.write(struct.pack('>i', value)[1:])

    def write_s32(self, value: int) -> None:
        self.write(struct.pack('>i', value))

    def write_s64(self, value: int) -> None:
        self.write(struct.pack('>q', value))

    def write_u8(self, value: int) -> None:
        self.write(struct.pack('B', value))

    def write_u16(self, value: int) -> None:
        self.write(struct.pack('>H', value))

    def write_u24(self, value: int) -> None:
        self.write(struct.pack('>I', value)[1:])

    def write_u32(self, value: int) -> None:
        self.write(struct.pack('>I', value))

    def write_u64(self, value: int) -> None:
        self.write(struct.pack('>Q', value))

    def write_f32(self, value: float) -> None:
        self.write(struct.pack('>f', value))

    def write_f64(self, value: float) -> None:
        self.write(struct.pack('>d', value))

    def write_string(self, value: str, size: Optional[int] = None) -> None:
        if size is None:
            self.write(value.encode('utf-8'))
            self.write_u8(0)
        else:
            i = 0
            for c in value:
                if i < size:
                    self.write_u8(ord(c))
                    i += 1
            while i < size:
                self.write_u8(0)
                i += 1

    def write_wstring(self, value: str, size: Optional[int] = None) -> None:
        if size is None:
            self.write(value.encode('utf-16be'))
            self.write_u16(0)
        else:
            i = 0
            for c in value:
                if i < size:
                    self.write_u16(ord(c))
                    i += 1
            while i < size:
                self.write_u16(0)
                i += 1

    def align_to(self, bits_count: int) -> None:
        self.write(b'\x00' * pad(self.tell(), bits_count))

    def tell(self) -> int:
        if self.writer is None:
            raise IOError(f'Stream was closed!')
        return self.writer.tell()

    def seek(self, off: int, origin: int) -> None:
        if self.writer is None:
            raise IOError(f'Stream was closed!')
        self.writer.seek(off, origin)

    def close(self) -> None:
        if self.writer is None:
            raise IOError(f'Stream was closed!')
        self.writer.close()
