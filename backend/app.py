from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Kisan Sathi Backend is Working!"


@app.route("/api/advice", methods=["POST"])
def advice():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Sawal bhejein."
        }), 400

    question = data.get("question")

    if not question:
        return jsonify({
            "status": "error",
            "message": "Sawal zaroor likhein."
        }), 400

    question = question.strip().lower()

    # -------------------------
    # Crop identify karna
    # -------------------------

    if "gandum" in question:
        crop = "Gandum"

    elif "chawal" in question:
        crop = "Chawal"

    elif "kapas" in question:
        crop = "Kapas"

    elif "makai" in question:
        crop = "Makai"

    elif "jowar" in question:
        crop = "Jowar"

    elif "til" in question:
        crop = "Til"

    else:
        crop = "Maloom nahi"


    # -------------------------
    # Sawal ka type identify karna
    # -------------------------

    if "pani" in question:
        question_type = "Pani"

    elif "khaad" in question:
        question_type = "Khaad"

    elif "bimari" in question:
        question_type = "Bimari"

    else:
        question_type = "Maloom nahi"


    # -------------------------
    # Simple jawab
    # -------------------------

    if crop == "Gandum" and question_type == "Pani":
        answer = "Gandum ko pani mitti ki halat dekh kar dein. Agar mitti zyada sookhi ho to pani dein."

    elif crop == "Gandum" and question_type == "Khaad":
        answer = "Gandum ke liye khaad mitti aur fasal ki zaroorat dekh kar deni chahiye."

    elif crop == "Gandum" and question_type == "Bimari":
        answer = "Agar Gandum mein bimari nazar aa rahi hai to pehle bimari ki nishaniyan check karein."

    elif crop == "Chawal" and question_type == "Pani":
        answer = "Chawal ko fasal ki zaroorat ke mutabiq pani dein. Zaroorat se zyada pani na dein."

    elif crop == "Kapas" and question_type == "Pani":
        answer = "Kapas ko zaroorat ke mutabiq pani dein aur mitti ko bohat zyada geela na rakhein."

    elif crop == "Makai" and question_type == "Pani":
        answer = "Makai ko waqt par pani dein. Mitti ko bohat zyada sookhne na dein."

    elif crop == "Jowar" and question_type == "Pani":
        answer = "Jowar ko fasal ki zaroorat ke mutabiq pani dein."

    elif crop == "Til" and question_type == "Pani":
        answer = "Til ko zaroorat ke mutabiq pani dein aur zyada pani se bachayein."

    else:
        answer = "Is sawal ke liye maloomat abhi hamare paas nahi hai."


    return jsonify({
        "status": "success",
        "sawal": question,
        "fasal": crop,
        "sawal_ka_type": question_type,
        "jawab": answer
    })


if __name__ == "__main__":
    app.run(debug=True)