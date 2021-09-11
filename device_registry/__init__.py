from flask import Flask, g, request
import os
import markdown
import shelve
from flask_restful import Resource, Api, reqparse

# Create Flask App - instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)
DEVICES = {}  # our DB :)
parser = reqparse.RequestParser()
parser.add_argument('identifier')  # add a variable to catch from request to task variable
parser.add_argument('name')  # add a variable to catch from request to task variable


@app.route("/")
def index():
    # Open README.md File
    with open(os.path.dirname(app.root_path) + '/README.md') as file:
        # read the content of the file
        content = file.read()
        # convert to HTML
        return markdown.markdown(content)


# update according to this example: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
# post and get for api useing flask_restful and get_json
class DeviceList(Resource):
    def get(self):
        return {'message': 'Success', 'data': DEVICES}, 200

    def post(self):
        args = parser.parse_args()

        DEVICES[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 20


api.add_resource(DeviceList, '/devices')
