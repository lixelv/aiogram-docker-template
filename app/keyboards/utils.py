def wrap(text, width=16, dots=3):
    if len(text) > width - dots:
        text = text[: width - dots] + "." * dots

    return text
