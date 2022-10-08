
class Note:
    def __init__(self, text: str, tags: list[str] = []) -> None:
        self.text = text
        self.tags = tags

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def add_tags(self, tags: list[str]):
        self.tags.extend(tags)

    def append(self, text: str):
        self.text += text

    def __contains__(self, other):
        if isinstance(other, str):
            return other.lower() in self.text.lower() or other.lower() in self.tags
        return False

    def __str__(self) -> str:
        tgs = ' '.join(self.tags) if self.tags else ' - '
        return 'Note: %s\n   Tags: %s' % (self.text, tgs)
