from src.adapters.orm import start_mappers
from src import app

if __name__ == "__main__":
    start_mappers()

    app.run()
