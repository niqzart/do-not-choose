from config import app
from simple import controller as simple_blueprint

app.register_blueprint(simple_blueprint)

if __name__ == "__main__":  # test only
    app.run(debug=True)
