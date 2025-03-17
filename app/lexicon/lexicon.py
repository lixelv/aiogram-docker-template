import json
from telegramify_markdown import markdownify


with open("app/lexicon/lexicon.json", "r") as f:
    lexicon = json.load(f)


def get_lexicon(command: str, language_code: str, *args, **kwargs) -> str:
    current_lexicon = lexicon[command]
    result = current_lexicon.get(language_code) or current_lexicon["en"]

    return markdownify(result.format(*args, **kwargs))


class Lexicon:
    def __init__(self, language_code: str):
        self.language_code = language_code

    def get(self, command: str, *args, **kwargs):
        return get_lexicon(command, self.language_code, *args, **kwargs)
