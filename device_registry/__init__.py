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


@app.route("/")
def index():
    # Open README.md File
    with open(os.path.dirname(app.root_path) + '/README.md') as file:
        # read the content of the file
        content = file.read()
        # convert to HTML
        return markdown.markdown(content)


# update according to this example: https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
# post and get for api using flask_restful and get_json
class DeviceList(Resource):
    # example: curl http://localhost:80//devices
    # for Postman use form-data
    def get(self):
        return {'message': 'Success', 'data': DEVICES}, 200

    # example: curl http://localhost:80//devices -d "identifier=123-456-789&name=new name" -X post -v
    def post(self):
        parser.add_argument('identifier', required=True, help="identifier is required")  # add a variable to catch from request to task variable
        parser.add_argument('name', required=True, help="name is required")  # add a variable to catch from request to task variable

        args = parser.parse_args()

        DEVICES[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 20


# get a device and delete a device
class Device(Resource):
    # example curl http://localhost:80//device/123-456-789
    def get(self, identifier):
        if not (identifier in DEVICES):
            return {'message': "Device not found", 'data': {}}, 404

        return {'message': 'Device found', 'data': DEVICES[identifier]}, 200

    # example: curl --location --request DELETE 'http://localhost:80//device/123-456-789'
    def delete(self, identifier):
        if not (identifier in DEVICES):
            return {'message': 'Device not found', 'data': {}}, 404

        del DEVICES[identifier]
        return '', 204


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
