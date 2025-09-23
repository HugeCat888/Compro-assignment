def fix_str(text):
    return text.encode("utf-8")

def decode_str(text):
    return text.decode("utf-8", "ignore").rstrip("\x00")