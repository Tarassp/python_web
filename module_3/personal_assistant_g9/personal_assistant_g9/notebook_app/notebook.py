from notebook_app.note import Note
from uuid import UUID
from collections import defaultdict


class Notebook:
    def __init__(self) -> None:
        self._notes: list[Note] = []

    def add(self, note: Note):
        self._notes.insert(0, note)

    def add_tags(self, tags: list[str], id: UUID) -> bool:
        note = self._get_note_by_id(id)
        if note is None:
            return False
        note.add_tags(tags)
        return True

    def remove(self, note: Note):
        self._notes.remove(note)

    def search_all(self, text: str) -> list[Note]:
        return list(filter(lambda note: text in note, self._notes))

    def search_by_tag(self, tag: str) -> list[Note]:
        return list(filter(lambda note: tag in note.tags, self._notes))

    def sort_by_tags(self) -> dict[str : list[Note]]:
        sort_dict = defaultdict(list)
        for note in self._notes:
            [sort_dict[tag].append(note) for tag in note.tags]
        return dict(sort_dict)

    def _get_note_by_id(self, id: UUID) -> Note | None:
        notes = list(filter(lambda note: id == note.id, self._notes))
        if len(notes) > 0:
            return notes[0]
        return None

    def __getitem__(self, index: int):
        if len(self._notes) > 0:
            return self._notes[index]
        return None

    def __len__(self):
        return len(self._notes)
