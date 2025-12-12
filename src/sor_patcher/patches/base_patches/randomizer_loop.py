from ...data import PATCHES
from ...file_formats.smd import SMD
from ...patches import Patch


class RandomizerLoop(Patch):
    def apply(self, smd: SMD) -> None:
        if "jmp_to_randomizer_loop" not in PATCHES.keys() or "randomizer_loop" not in PATCHES.keys():
            raise RuntimeError("Couldn't find jmp_to_randomizer_loop or randomizer_loop in patches!")

        # post hook vblank to jump to our randomizer loop
        smd.patch(
            PATCHES["jmp_to_randomizer_loop"]["address"],
            PATCHES["jmp_to_randomizer_loop"]["data"],
        )

        smd.patch(
            PATCHES["randomizer_loop"]["address"],
            PATCHES["randomizer_loop"]["data"],
        )