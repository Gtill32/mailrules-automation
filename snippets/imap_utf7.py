"""
Пример одной из нетривиальных задач проекта: IMAP требует кодировку
Modified UTF-7 для названий папок с не-ASCII символами (например, кириллицей).
Стандартная библиотека Python не предоставляет готового решения для этого формата.
"""
import base64


def decode_imap_utf7(s: str) -> str:
    """Декодирует названия папок IMAP из Modified UTF-7 в Unicode."""
    if "&" not in s:
        return s
    result = []
    i = 0
    while i < len(s):
        if s[i] == "&":
            j = s.index("-", i + 1)
            b64 = s[i+1:j]
            if b64 == "":
                result.append("&")
            else:
                b64 = b64.replace(",", "/")
                pad = (4 - len(b64) % 4) % 4
                b64 += "=" * pad
                decoded = base64.b64decode(b64).decode("utf-16-be")
                result.append(decoded)
            i = j + 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)


def encode_imap_utf7(s: str) -> str:
    """Кодирует Unicode-название папки в Modified UTF-7 для IMAP."""
    result = []
    buf = []

    def flush_buf():
        if buf:
            b64 = base64.b64encode(''.join(buf).encode('utf-16-be')).decode('ascii')
            b64 = b64.replace('/', ',').rstrip('=')
            result.append('&' + b64 + '-')
            buf.clear()

    for ch in s:
        if 0x20 <= ord(ch) <= 0x7e and ch != '&':
            flush_buf()
            result.append(ch)
        elif ch == '&':
            flush_buf()
            result.append('&-')
        else:
            buf.append(ch)

    flush_buf()
    return ''.join(result)
