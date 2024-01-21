from import_reqs import *

@app.route("/test")
async def test():
    doc = QUESTIONS.document("abcdefg").get()
    print(f"data:{doc.to_dict()}")
    return "Hello World"

@app.route("/queryQuestion/<id>", methods=["GET"])
async def queryQuestion(id):
    """
    queryQuestion(): The queryQuestion Page for the API
    """
    try:
        # data = await request.get_json()
        doc = QUESTIONS.document(id).get()
        if doc.exists:
            question_data = doc.to_dict()

            return jsonify({
                "questionID": id,
                "numResponses": question_data.get("numResponses"),
                "question": question_data.get("question"),
                "responses": question_data.get("responses")
            })

        else:
            return jsonify({"error": "Question not found"}), 404
        

    except Exception as e:
        print(e)
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500