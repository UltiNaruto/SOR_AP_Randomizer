from ...data import PATCHES
from ...file_formats.smd import SMD
from ...patches import Patch


class SkipToOptions(Patch):
    def apply(self, smd: SMD) -> None:
        if "skip_to_main_menu" not in PATCHES.keys() or "skip_to_options" not in PATCHES.keys():
            raise RuntimeError("Couldn't find skip_to_main_menu or skip_to_options in patches!")

        # skips to main menu directly
        smd.patch(
            PATCHES["skip_to_main_menu"]["address"],
            PATCHES["skip_to_main_menu"]["data"],
        )

        # skips to options then
        smd.patch(
            PATCHES["skip_to_options"]["address"],
            PATCHES["skip_to_options"]["data"],
        )