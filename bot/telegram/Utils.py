def markup_clearner(text: str):
    especial_characters = [
        '_', '*', '[', ']', '(', ')',
        '~', '`', '>', '#', '+', '-',
         '=', '|', '{', '}', '.', '!'
    ]
    for ch in especial_characters:
        text = text.replace( ch , '\\' + ch)
    return text

    