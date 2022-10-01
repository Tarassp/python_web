from notebook_app.note import Note
from notebook_app.notebook import Notebook
from shared.client import Service
from shared.cli_command import CLICommand
from shared.status import Status
from shared.error_decorator import *
from shared.local_storage import Storage


class NotebookService(Service):
    def __init__(self, storage: Storage, notes: Notebook) -> None:
        self._notebook = notes
        self._searched_notes: list[Note] = []
        self._selected_note: Note | None = None
        self._storage = storage
        self._handlers = {
            CLICommand.ADD: self._handle_add,
            CLICommand.TAGS: self._handle_add_tags,
            CLICommand.SELECTREQUEST: self._handle_select_request,
            CLICommand.SELECT: self._handle_select_note,
            CLICommand.SHOW: self._handle_show_all,
            CLICommand.SHOWSELECTED: self._handle_show_selected,
            CLICommand.SEARCH: self._handle_search,
            CLICommand.SEARCHBYTAG: self._handle_search_by_tag,
            CLICommand.SEARCHSELECTING: self._handle_search_selecting,
            CLICommand.SORTBYTAGS: self._handle_sort_by_tags,
            CLICommand.DELETE: self._handle_delete,
            CLICommand.CHANGE: self._handle_change,
            CLICommand.EXIT: self._handle_exit,
            CLICommand.HELP: self._handle_help,
            CLICommand.UNKNOWN: self._handle_unknown,
        }

    @input_error
    def _get_handler(self, command: CLICommand):
        if command is CLICommand.UNKNOWN:
            raise UnknownAssistentCommand
        return self._handlers[command]

    def handle(self, command: CLICommand, value: list[str]) -> Status:
        handler = self._get_handler(command)
        return handler(value)

    @input_error
    def _handle_add(self, value: list[str]) -> Status:
        if len(value) < 1:
            raise UnknownAssistentValue("Note cannot be empty!")
        self._selected_note = Note(" ".join(value), [])
        self._notebook.add(self._selected_note)
        request = Status.Request("Enter some tag(s) for your note: ", CLICommand.TAGS)
        self._storage.save(self._notebook)
        return Status("Note is added successfully!", request)

    def _handle_add_tags(self, tags: list[str]) -> Status:
        if self._selected_note:
            self._selected_note.add_tags(tags)
        else:
            return Status(
                "You didn't select note yet. Please use SELECT command first."
            )
        self._selected_note = None
        if not tags:
            return Status("You skipped adding tags")
        self._storage.save(self._notebook)
        if len(tags) > 1:
            return Status("Tags are added successfully!")
        return Status("Tag is added successfully!")

    def _handle_select_request(self, value: list[str]) -> Status:
        if not len(self._notebook):
            return Status("Notebook is empty. Add some note first.")
        if len(value) == 1 and int(value[0]) <= len(self._notebook):
            return self._handle_select_note(value)
        request = Status.Request(
            'Enter some text to find notes or just hit "Enter" to show all notes: ',
            CLICommand.SEARCHSELECTING,
        )
        return Status(request=request)

    def _handle_search_selecting(self, value: list[str]) -> Status:
        search_status = self._handle_search(value)
        if search_status.response.lower() != "no results":
            search_status.request = Status.Request(
                "Enter the note number: ", CLICommand.SELECT
            )
        return search_status

    def _handle_select_note(self, value: list[str]) -> Status:
        note_number = int(value[0])
        if (note_number - 1) < len(self._searched_notes):
            self._selected_note = self._searched_notes[note_number - 1]
        elif note_number <= len(self._notebook):
            self._selected_note = self._notebook[note_number - 1]
        else:
            if len(self._notebook) == 0:
                return Status("Cannot select the note because Notebook is empty.")
            else:
                return Status("You entered wrong record number.")
        return Status(
            f"{self._selected_note}\nUse <TAGS>, <CHANGE>, or <DELETE> command to work on it"
        )

    @input_error
    def _handle_search(self, value: list[str]) -> Status:
        searched_text = " ".join(value)
        self._searched_notes = self._notebook.search_all(searched_text)
        if self._searched_notes:
            message = ""
            for i, v in enumerate(self._searched_notes):
                message += f"{i + 1}. {v}\n"
            message.strip("\n")
            message = "----------------------\n" + message + "----------------------"
            return Status(message)
        return Status("No Results")

    @input_error
    def _handle_search_by_tag(self, value: list[str]) -> Status:
        searched_text_tag = " ".join(value)
        self._searched_notes = self._notebook.search_by_tag(searched_text_tag)
        if self._searched_notes:
            message = ""
            for i, v in enumerate(self._searched_notes):
                message += f"{i + 1}. {v}\n"
            message.strip("\n")
            message = "----------------------\n" + message + "----------------------"
            return Status(message)
        return Status("No Results")

    def _handle_sort_by_tags(self, value) -> Status:
        sort_by_tags_dict: dict[str : list[Note]] = self._notebook.sort_by_tags()
        message = ""
        for tag, notes in sort_by_tags_dict.items():
            message += f"Notes by tag '{tag}':\n"
            for i, v in enumerate(notes):
                message += f"{i + 1}. {v}\n"

        message.strip("\n")
        if not message:
            message = "Note List is empty!\n"
        message = "----------------------\n" + message + "----------------------"
        return Status(message)

    def _handle_delete(self, value) -> Status:
        if self._selected_note:
            self._notebook.remove(self._selected_note)
            self._selected_note = None
            self._storage.save(self._notebook)
            return Status("Note is deleted successfully!")
        return Status("You didn't select note yet. Please use SELECT command first.")

    def _handle_change(self, value: list[str]) -> Status:
        if self._selected_note:
            self._selected_note.append(" ".join(value))
            self._selected_note = None
            self._storage.save(self._notebook)
            return Status("Note is changed successfully!")
        return Status("You didn't select note yet. Please use SELECT command first.")

    def _handle_show_selected(self, value) -> Status:
        if self._selected_note:
            return Status(str(self._selected_note))
        return Status("You didn't select record yet. Please use SELECT command first.")

    @input_error
    def _handle_show_all(self, value) -> Status:
        message = ""
        for i, v in enumerate(self._notebook._notes):
            message += f"{i + 1}. {v}\n"

        message.strip("\n")
        if not message:
            message = "Note List is empty!\n"
        message = "----------------------\n" + message + "----------------------"
        self._searched_notes = self._notebook._notes
        return Status(message)

    @input_error
    def _handle_exit(self, value) -> Status:
        return Status("Good bye!")

    @input_error
    def _handle_help(self, value) -> Status:
        commands = [
            "ADD <note>",
            "TAGS <tag1, tag2 ...>",
            "SELECT",
            "SELECT <number of note>",
            "CHANGE <text>" "SEARCH <text>",
            "SEARCH TAG <tag>" "SORT TAGS",
            "SELECTED",
            "DELETE",
            "SHOW ALL",
            "GOOD BYE",
            "CLOSE",
            "EXIT",
        ]
        return Status("\n".join(commands))

    @input_error
    def _handle_unknown(value) -> Status:
        return Status("Incorrect Command!!!")
