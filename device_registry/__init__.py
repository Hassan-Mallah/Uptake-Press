from flask import Flask
import os
import markdown

# Create Flask App - instance of Flask
app = Flask(__name__)

@app.route("/")
def index():
    """ Present some documentation """

    # Open README.md File
    with open(os.path.dirname(app.root_path) + '/README.md') as file:
        content = file.read()
        return markdown.markdown(content)