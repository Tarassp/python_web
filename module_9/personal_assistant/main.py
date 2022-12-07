from adapters import orm
from presentation_layer.cli.client import Client
from domain.model import User

SOME_USER = User(name="Someuser", user_id="user_root")

if __name__ == "__main__":
    orm.start_mappers()
    client = Client(SOME_USER)
    client.run()
