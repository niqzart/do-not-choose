from basic import simple_blueprint, reglog_blueprint
from config import app

app.register_blueprint(simple_blueprint)
app.register_blueprint(reglog_blueprint)

if __name__ == "__main__":  # test only
    app.run(debug=True)
