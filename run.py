import os
from app import app


if __name__ == '__main__':
    print(os.environ['APP_SETTINGS'])
    app.run()
