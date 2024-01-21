from import_reqs import *

@app.route("/test")
async def test():
    doc = QUESTIONS.document("abcdefg").get()
    print(f"data:{doc.to_dict()}")
    return "Hello World"


@app.route("/likeResponse/<qid>/<rid>/<uid>", methods=["GET"])
async def likeResponse(qid, rid, uid):
    """
    qid: question id
    rid: response id
    uid: user id

    likeResponse(): The likeResponse Page for the API
    add the user to the list of users who liked the response
    add to numLikes
    """
    try:
        # data = await request.get_json()
        qdoc = QUESTIONS.document(qid).get()
        qdoc_ref = QUESTIONS.document(qid)
        udoc = USERS.document(uid).get()
        if qdoc.exists and udoc.exists:
            question_data = qdoc.to_dict()
            username = udoc.to_dict().get("username")
            responses = question_data.get("responses")

            likedBy = responses[rid]["likedBy"]
            numLikes = responses[rid]["numLikes"]

            likedBy.append(username)
            responses[rid]["numLikes"] = numLikes + 1

            qdoc_ref.update({
                "responses": responses
                
            })

            return jsonify({
                "response": responses.get(rid)
            })

        else:
            return jsonify({"error": "Something not found", "qdoc": qdoc.exists, "udoc": udoc.exists}), 404
        

    except Exception as e:
        print(e)
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500

@app.route("/unlikeResponse/<qid>/<rid>/<uid>", methods=["GET"])
async def unlikeResponse(qid, rid, uid):
    """
    qid: question id
    rid: response id
    uid: user id

    likeResponse(): The likeResponse Page for the API
    subtract the user from the list of users who liked the response
    subtract from numLikes
    """
    try:
        # data = await request.get_json()
        qdoc = QUESTIONS.document(qid).get()
        qdoc_ref = QUESTIONS.document(qid)
        udoc = USERS.document(uid).get()
        if qdoc.exists and udoc.exists:
            question_data = qdoc.to_dict()
            username = udoc.to_dict().get("username")
            responses = question_data.get("responses")

            likedBy = responses[rid]["likedBy"]
            numLikes = responses[rid]["numLikes"]

            likedBy.remove(username)
            responses[rid]["numLikes"] = numLikes - 1

            qdoc_ref.update({
                "responses": responses
                
            })

            return jsonify({
                "response": responses.get(rid)
            })

        else:
            return jsonify({"error": "Something not found", "qdoc": qdoc.exists, "udoc": udoc.exists}), 404
        

    except Exception as e:
        print(e)
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500


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