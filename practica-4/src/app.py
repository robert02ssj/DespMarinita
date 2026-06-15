from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hola Mundo</h1>"


@app.route("/about")
def about():
    return "<h1>Acerca de</h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
