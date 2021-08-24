from flask import Flask, g, request
import os
import markdown
import shelve
from flask_restful import Resource, Api

# Create Flask App - instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db


@app.route("/")
def index():
    # Open README.md File
    with open(os.path.dirname(app.root_path) + '/README.md') as file:
        # read the content of the file
        content = file.read()
        # convert to HTML
        return markdown.markdown(content)


# post and get for api
class DeviceList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        args = request.get_json(force=True)

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 20


api.add_resource(DeviceList, '/devices')