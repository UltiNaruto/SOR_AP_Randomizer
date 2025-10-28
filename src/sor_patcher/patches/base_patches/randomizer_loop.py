from ...data.patches import (
    JMP_TO_RANDOMIZER_LOOP_ADDRESS,
    JMP_TO_RANDOMIZER_LOOP_BYTES,
    RANDOMIZER_LOOP_ADDRESS,
    RANDOMIZER_LOOP_BYTES,
)
from ...file_formats.smd import SMD
from ...patches import Patch


class RandomizerLoop(Patch):
    def apply(self, smd: SMD) -> None:
        # post hook vblank to jump to our randomizer loop
        smd.patch(
            JMP_TO_RANDOMIZER_LOOP_ADDRESS,
            JMP_TO_RANDOMIZER_LOOP_BYTES,
        )

        smd.patch(
            RANDOMIZER_LOOP_ADDRESS,
            RANDOMIZER_LOOP_BYTES,
        )