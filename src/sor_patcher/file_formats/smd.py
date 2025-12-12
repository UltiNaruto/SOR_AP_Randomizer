import struct
from enum import IntEnum

from ..utils.buffered_reader_be import BufferedReaderBE
from ..utils.buffered_writer_be import BufferedWriterBE
from ..utils.byteutils import replace_bytes_at
from ..utils.parser import StructParser


class SerialNumber(StructParser):
    software_type: str
    serial_number: int
    revision: int

    def __len__(self):
        return 2 + 1 + 8 + 1 + 2

    def read(self, reader: BufferedReaderBE) -> None:
        self.software_type = reader.read_string(2)
        if reader.read_string(1) != ' ':
            raise RuntimeError('Invalid Serial Number in Rom Header!')
        self.serial_number = int(reader.read_string(8), 16)
        if reader.read_string(1) != '-':
            raise RuntimeError('Invalid Serial Number in Rom Header!')
        self.revision = int(reader.read_string(2), 16)

    def write(self, writer: BufferedWriterBE) -> None:
        writer.write_string(str(self), 14)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.software_type} {self.serial_number:08X}-{self.revision:02X}'


class AddressRange(StructParser):
    start: int
    end: int

    def __len__(self):
        return 4 + 4

    def read(self, reader: BufferedReaderBE) -> None:
        self.start = reader.read_u32()
        self.end = reader.read_u32()

    def write(self, writer: BufferedWriterBE) -> None:
        writer.write_u32(self.start)
        writer.write_u32(self.end)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.start:08X}-{self.end:08X}'


class RamType(IntEnum):
    NoSave16Bit = 0xA0
    NoSave8BitEven = 0xB0
    NoSave8BitOdd = 0xB8
    Save16Bit = 0xE0
    Save8BitEven = 0xF0
    Save8BitOdd = 0xF8

class ExtraMemory(StructParser):
    magic_number: str
    ram_type: RamType
    address_range: AddressRange

    def __init__(self):
        super().__init__()

        self.address_range = AddressRange()

    def __len__(self):
        return 2 + 1 + 1 + len(self.address_range)

    def read(self, reader: BufferedReaderBE) -> None:
        self.magic_number = reader.read_string(2).rstrip(' ')
        if self.magic_number != 'RA':
            reader.seek(10, 1)
            return
        self.ram_type = RamType(reader.read_u8())
        if reader.read_string(1) != ' ':
            raise RuntimeError('Invalid Extra Memory in Rom Header!')
        self.address_range.read(reader)

    def write(self, writer: BufferedWriterBE) -> None:
        if self.magic_number == 'RA':
            writer.write_string(self.magic_number, 2)
            writer.write_u8(int(self.ram_type))
            writer.write(b' ')
            self.address_range.write(writer)
        else:
            ExtraMemory.write_empty(writer)

    @staticmethod
    def write_empty(writer: BufferedWriterBE):
        writer.write(b' ' * 12)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.address_range.start:08X}-{self.address_range.end:08X} (ram type: {str(self.ram_type)})'


class RegionAndMicrophone(IntEnum):
    JpnNoMic = 0x00
    JpnMic = 0x10
    OverseasNoMic = 0x20
    OverseasMic = 0x30
    BothNoMic = 0x40
    BothMic = 0x50
    JpnNoMic_OverseasMic = 0x60
    JpnMic_OverseasNoMic = 0x70


class ModemSupport(StructParser):
    magic_number: str
    publisher: str
    game_number: int
    version: int
    region_and_microphone: RegionAndMicrophone

    def __len__(self):
        return 2 + 4 + 2 + 1 + 1 + 2

    def read(self, reader: BufferedReaderBE) -> None:
        self.magic_number = reader.read_string(2).rstrip(' ')
        if self.magic_number != 'M0':
            reader.seek(10, 1)
            return
        self.publisher = reader.read_string(4).rstrip(' ')
        self.game_number = int(reader.read_string(2).rstrip(' '), 16)
        if reader.read_string(1) not in [',', '.']:
            raise RuntimeError('Invalid Modem Support in Rom Header!')
        self.version = int(reader.read_string(1).rstrip(' '), 16)
        self.region_and_microphone = RegionAndMicrophone(int(reader.read_string(2).rstrip(' '), 16))

    def write(self, writer: BufferedWriterBE) -> None:
        if self.magic_number == 'M0':
            writer.write_string(self.magic_number, 2)
            writer.write_string(f'{self.publisher:04X}', 2)
            writer.write_string(f'{self.game_number:02X}', 2)
            writer.write(b',')
            writer.write_string(f'{self.version:01X}', 2)
            writer.write_string(f'{int(self.region_and_microphone):02X}', 2)
        else:
            ModemSupport.write_empty(writer)

    @staticmethod
    def write_empty(writer: BufferedWriterBE):
        writer.write(b' ' * 12)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.magic_number}{self.publisher:04X}{self.game_number:02X},{self.version:01X}{int(self.region_and_microphone):02X}'


class SMDHeader(StructParser):
    system_type: str
    copyright_release_date: str
    domestic_game_title: str
    overseas_game_title: str
    serial_number: SerialNumber
    checksum: int
    device_support: str
    rom_address_range: AddressRange
    ram_address_range: AddressRange
    extra_memory: ExtraMemory
    modem_support: ModemSupport
    region_support: str

    def __init__(self):
        super().__init__()

        self.serial_number = SerialNumber()
        self.rom_address_range = AddressRange()
        self.ram_address_range = AddressRange()
        self.extra_memory = ExtraMemory()
        self.modem_support = ModemSupport()

    def __len__(self):
        len_ = 16
        len_ += 16
        len_ += 48
        len_ += 48
        len_ += len(self.serial_number)
        len_ += 2
        len_ += 16
        len_ += len(self.rom_address_range)
        len_ += len(self.ram_address_range)
        len_ += len(self.extra_memory)
        len_ += len(self.modem_support)
        len_ += 40
        len_ += 3
        len_ += 13

        return len_

    def read(self, reader: BufferedReaderBE) -> None:
        self.system_type = reader.read_string(16).rstrip(' ')
        self.copyright_release_date = reader.read_string(16).rstrip(' ')
        self.domestic_game_title = reader.read_string(48).rstrip(' ')
        self.overseas_game_title = reader.read_string(48).rstrip(' ')
        self.serial_number.read(reader)
        self.checksum = reader.read_u16()
        self.device_support = reader.read_string(16).rstrip(' ')
        self.rom_address_range.read(reader)
        self.ram_address_range.read(reader)
        self.extra_memory.read(reader)
        self.modem_support.read(reader)
        reader.seek(40, 1)
        self.region_support = reader.read_string(3).strip(' ')
        reader.seek(13, 1)

    def write(self, writer: BufferedWriterBE) -> None:
        write_padded_string = lambda s, l: [
            *[
                writer.write(bytes(s[i], 'utf-8'))
                for i in range(len(s))
            ],
            *[
                 writer.write(b' ')
                 for _ in range(len(s), l)
            ]
        ]

        write_padded_string(self.system_type, 16)
        write_padded_string(self.copyright_release_date, 16)
        write_padded_string(self.domestic_game_title, 48)
        write_padded_string(self.overseas_game_title, 48)
        self.serial_number.write(writer)
        writer.write_u16(self.checksum)
        write_padded_string(self.device_support, 16)
        self.rom_address_range.write(writer)
        self.ram_address_range.write(writer)
        self.extra_memory.write(writer)
        self.modem_support.write(writer)
        write_padded_string('', 40)
        write_padded_string(self.region_support, 3)
        write_padded_string('', 13)


class SMD(StructParser):
    unknown: bytes
    header: SMDHeader
    datas: bytes

    def __init__(self):
        super().__init__()

        self.header = SMDHeader()

    def __len__(self):
        len_ = len(self.unknown)
        len_ += len(self.header)
        len_ += len(self.datas)

        return len_

    def read(self, reader: BufferedReaderBE) -> None:
        reader.seek(0, 2)
        size = reader.tell()
        reader.seek(0, 0)

        self.unknown = reader.read(256)
        self.header.read(reader)
        self.datas = reader.read(size - reader.tell())

    def write(self, writer: BufferedWriterBE) -> None:
        self.fix_checksum()

        writer.write(self.unknown[0:256])
        self.header.write(writer)
        writer.write(self.datas)

    def fix_checksum(self):
        checksum = 0
        for i in range(len(self.datas) // 2):
            checksum += struct.unpack('>H', self.datas[2*i:2*(i+1)])[0]
            checksum &= 0xffff
        self.header.checksum = checksum

    def patch(self, address: int, asm: bytes) -> None:
        if self.header.rom_address_range.end < address < 0x200:
            raise RuntimeError(f'Invalid address in ROM! (at: 0x{address:08X})')

        self.datas = replace_bytes_at(self.datas, address - 0x200, asm)
