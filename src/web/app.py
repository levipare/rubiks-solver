from flask import Flask, render_template, Response

app = Flask(__name__)


def start():
    app.run()


camera_count = 0


def create_camera_feed(gen):
    """
    Creates a camera route that provides a stream of frames given by the provided generator `gen`.
    @param gen a generator yielding frames
    """
    global camera_count

    @app.route(f"/camera/{camera_count}")
    def feed():
        return Response(
            gen,
            mimetype="multipart/x-mixed-replace; boundary=frame",
        )

    camera_count += 1


def bind_solve_fn(solve_fn):
    """
    Creates a endpoint to register a user initiated `solve` event.
    @param solve_fn a function that is called when a POST to /solve is registered
    """

    @app.route(f"/solve")
    def solve():
        solve_fn()
        return Response(status=200)


@app.route("/")
def index():
    return render_template(
        "index.html",
        num_cams=camera_count,
    )
