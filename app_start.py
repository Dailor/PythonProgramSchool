from app import init_app

init_app()

from app import app

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"])
