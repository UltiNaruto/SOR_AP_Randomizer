from ...data.patches import (
    # skip to main menu from logo
    SKIP_TO_MAIN_MENU_ADDRESS,
    SKIP_TO_MAIN_MENU_BYTES,

    # skip to options from main menu
    SKIP_TO_OPTIONS_ADDRESS,
    SKIP_TO_OPTIONS_BYTES,
)
from ...file_formats.smd import SMD
from ...patches import Patch


class SkipToOptions(Patch):
    def apply(self, smd: SMD) -> None:
        # skips to main menu directly
        smd.patch(
            SKIP_TO_MAIN_MENU_ADDRESS,
            SKIP_TO_MAIN_MENU_BYTES
        )

        # skips to options then
        smd.patch(
            SKIP_TO_OPTIONS_ADDRESS,
            SKIP_TO_OPTIONS_BYTES,
        )