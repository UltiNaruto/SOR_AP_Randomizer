from ...data import PATCHES
from ...file_formats.smd import SMD
from ...patches import Patch


class UtilsFunctions(Patch):
    def apply(self, smd: SMD) -> None:
        if "utils_functions" not in PATCHES.keys():
            raise RuntimeError("Couldn't find utils_functions in patches!")

        # utils functions that will be used for various things
        smd.patch(
            PATCHES["utils_functions"]["address"],
            PATCHES["utils_functions"]["data"],
        )