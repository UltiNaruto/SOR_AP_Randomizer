from ...data.patches import (
    # utils functions that will be used for various things
    UTILS_FUNCTIONS_ADDRESS,
    UTILS_FUNCTIONS_LOOP_BYTES,
)
from ...file_formats.smd import SMD
from ...patches import Patch


class UtilsFunctions(Patch):
    def apply(self, smd: SMD) -> None:
        # utils functions that will be used for various things
        smd.patch(
            UTILS_FUNCTIONS_ADDRESS,
            UTILS_FUNCTIONS_LOOP_BYTES
        )