def replace_bytes_at(src: bytes, at: int, datas: bytes) -> bytes:
    tmp = src[:at]
    tmp += datas
    tmp += src[at+len(datas):]
    return tmp