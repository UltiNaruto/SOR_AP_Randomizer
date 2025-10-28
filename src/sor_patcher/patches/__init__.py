from abc import ABCMeta, abstractmethod

from ..file_formats.smd import SMD


class Patch(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, smd: SMD) -> None:
        raise NotImplementedError