from app import get_app

app = get_app()
if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"])
