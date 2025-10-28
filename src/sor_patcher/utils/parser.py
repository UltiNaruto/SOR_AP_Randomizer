from __future__ import annotations

from abc import ABCMeta, abstractmethod

from .buffered_reader_be import BufferedReaderBE
from .buffered_writer_be import BufferedWriterBE


class StructParser(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def read(self, reader: BufferedReaderBE) -> None:
        raise NotImplementedError

    @abstractmethod
    def write(self, writer: BufferedWriterBE) -> None:
        raise NotImplementedError
