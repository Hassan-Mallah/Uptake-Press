from flask import Flask, g
import os
import markdown
import shelve

# Create Flask App - instance of Flask
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    # Open README.md File
    with open(os.path.dirname(app.root_path) + '/README.md') as file:
        # read the content of the file
        content = file.read()
        # convert to HTML
        return markdown.markdown(content)