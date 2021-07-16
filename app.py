from flask import Flask

app = Flask(__name__)

# declare constants
HOST = "0.0.0.0"
PORT = 5000


# from api.queue import queue_monitor
from api.projecting_return import projecting_return
from api.restplus import api

api.init_app(app)
# api.add_namespace(queue_monitor)
api.add_namespace(projecting_return)


if __name__ == "__main__":
    app.run(host=HOST, debug=True, port=PORT)
