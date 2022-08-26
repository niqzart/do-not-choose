from config import app
from simple import controller as simple_namespace

api = app.configure_restx()

api.add_namespace(simple_namespace)

if __name__ == "__main__":  # test only
    app.run(debug=True)
