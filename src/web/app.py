from flask import Flask, render_template, Response

app = Flask(__name__)


camera_feeds = {}

@app.route("/camera/<key>")
def feed(key):
    try:
        return Response(
            camera_feeds[key],
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )
    except KeyError:
        return Response(status=404)

def add_camera_feed(gen, key):
    """
    Add a new camera feed that can be accessed by its key.
    @param gen a generator yielding frames
    @param key a unique identifier for the camera feed
    """
    camera_feeds[key] = gen



def bind_solve_fn(solve_fn):
    """
    Creates an endpoint to register a cleint initiated `solve` event.
    @param solve_fn a function that is called when a POST to /solve is received
    """

    @app.route(f"/solve", methods=["POST"])
    def solve():
        return Response(status= 200 if solve_fn() else 500)


def bind_scramble_fn(scramble_fn):
    """
    Creates an endpoint to register a client initiated `scramble` event.
    @param scramble_fn a function that is called when a POST to /scramble is received
    """

    @app.route(f"/scramble", methods=["POST"])
    def scramble():
        return Response(status= 200 if scramble_fn() else 500)
    
def bind_abort_fn(abort_fn):
    """
    Creates an endpoint to register a client initiated `abort` event.
    @param abort_fn a function that is called when a POST to /abort is received
    """

    @app.route(f"/abort", methods=["POST"])
    def abort():
        return Response(status= 200 if abort_fn() else 500)

@app.route("/")
def index():
    return render_template("index.html")
    
def start(debug = False):
    """
    Start the flask server with option to run in debug mode.
    """
    app.debug = debug
    app.run(host='0.0.0.0', port=5000)
