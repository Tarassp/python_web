import pathlib
from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).parent.parent
config = dotenv_values('.env')


class Config:
    UPLOAD_FOLDERS = BASE_DIR / 'uploads'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / 'app.db.sqlite')
    SECRET_KEY = config['SECRET_KEY']
    
app_config = Config()