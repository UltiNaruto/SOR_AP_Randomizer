def _is_bits_dividable_by_two(bits: int | float) -> bool:
    if bits / 2 == 1:
        return True
    if int(bits / 2) != float(bits / 2):
        return False
    return _is_bits_dividable_by_two(bits / 2)

def pad(size: int, bits: int) -> int:
    if not _is_bits_dividable_by_two(bits):
        raise RuntimeError(f'Cannot pad to {bits} bits!')
    return (bits - (size % bits)) & (bits - 1)

def pad32(size: int) -> int:
    return pad(size, 32)

def pad64(size: int) -> int:
    return pad(size, 64)
