from flask_restx import Resource, inputs
from flask_restx.reqparse import RequestParser

from __lib__.flask_fullstack import ResourceController, PydanticModel
from config import sessionmaker

controller = ResourceController("simple", sessionmaker=sessionmaker)


class SimpleModel(PydanticModel):
    message: str


@controller.route("/")
class SimpleResource(Resource):
    @controller.marshal_with(SimpleModel)
    def get(self):
        return SimpleModel(message="Hello World")

    parser = RequestParser()
    parser.add_argument("error", type=inputs.boolean, default=False,
                        help="If true will cause a 500 error")

    @controller.doc_abort(500, "You asked to raise an error")
    @controller.argument_parser(parser)
    @controller.marshal_with(SimpleModel)
    def post(self, *, error: bool):
        if error:
            raise ValueError("User requested an error")
        return SimpleModel(message="I'm fine"), 201
