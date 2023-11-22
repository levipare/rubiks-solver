from flask import Flask, render_template, Response

app = Flask(__name__)


camera_feeds = {}

@app.route("/camera/<key>")
def feed(key):
    return Response(
        camera_feeds[key],
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

def add_camera_feed(gen, key):
    """
    Add a new camera feed that can be accessed by its key.
    @param gen a generator yielding frames
    @param key a unique identifier for the camera feed
    """
    camera_feeds[key] = gen



def bind_solve_fn(solve_fn):
    """
    Creates a endpoint to register a user initiated `solve` event.
    @param solve_fn a function that is called when a POST to /solve is registered
    """

    @app.route(f"/solve", methods=["POST"])
    def solve():
        return Response(status= 200 if solve_fn() else 500)
    

@app.route("/")
def index():
    return render_template("index.html")
    
def start(debug = False):
    """
    Start the flask server with option to run in debug mode.
    """
    app.debug = debug
    app.run(host='0.0.0.0', port=5000)
