lexicon = {
    "start": {"ru": "Привет!", "en": "Hello!"},
    "test": {"ru": "Привет, напиши что-то!", "en": "Hello, write something!"},
}


def get_lexicon(command: str, language_code: str):
    current_lexicon = lexicon[command]
    return current_lexicon.get(language_code) or current_lexicon["en"]
