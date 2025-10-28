from ...data.patches import (
    TIMEOUT_CLIENT_FUNC_ADDRESS,
    TIMEOUT_CLIENT_FUNC_BYTES,
)
from ...file_formats.smd import SMD
from ...patches import Patch


class TimeoutClientFunc(Patch):
    def apply(self, smd: SMD) -> None:
        smd.patch(
            TIMEOUT_CLIENT_FUNC_ADDRESS,
            TIMEOUT_CLIENT_FUNC_BYTES,
        )