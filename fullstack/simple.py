from flask_restx import Resource

from __lib__.flask_fullstack import ResourceController
from config import sessionmaker

controller = ResourceController("simple", sessionmaker=sessionmaker)


@controller.route("/")
class SimpleResource(Resource):
    def get(self):
        return "Hello World"
