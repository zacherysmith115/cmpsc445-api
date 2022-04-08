from connexion import FlaskApp
from controllers import Application

if __name__ == "__main__":
    app: FlaskApp = Application()
    app.run(port=8080, debug=True)
