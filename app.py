from import_reqs import *
import endpoints.core as core

PORT = 7001


@app.route("/", methods=["GET"])
async def home():
    return "<h1> CEREBRUS HOME - IF YOU SEE THIS WE UP NOW </h1>"


@app.route("/health", methods=["GET"])
async def health():
    """
    Health(): The Health Page for the API
    """
    return jsonify(
        {
            "success": True,
        }
    ), 200


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", PORT)),
        debug=True,
        use_reloader=False,
        threaded=True,
    )

    print("Done!")
