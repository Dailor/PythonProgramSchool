from app import init_app

app = init_app()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"])
