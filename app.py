from flask import Flask, render_template

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")


@app.route("/")
def index():
    return render_template('index.html')
