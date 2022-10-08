from shared.client import Client
from shared.local_storage import LocalStorage
from shared.service import Service
from notebook_app.notebook import Notebook
from notebook_app.notebook_service import NotebookService


class NotebookClient(Client):
    @property
    def message(self) -> str:
        return "Welcome to NoteBook App!\nEnter the command or type 'help' to see the list of commands: "

    def create_service(self) -> Service:
        storage = LocalStorage("notebook")
        notes = storage.load() or Notebook()
        return NotebookService(storage, notes)
