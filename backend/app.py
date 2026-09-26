from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Kisan Sathi Backend is Working!"


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "success",
        "message": "Kisan Sathi backend is running."
    })


def normalize_question(question):
    question = question.strip().lower()

    replacements = {
        "paani": "pani",
        "panie": "pani",
        "gandum": "gandum",
        "gehoon": "gandum",
        "gehun": "gandum",
        "chawal": "chawal",
        "kapas": "kapas",
        "cotton": "kapas",
        "makai": "makai",
        "maize": "makai",
        "jowar": "jowar",
        "sorghum": "jowar",
        "til": "til",
        "sesame": "til"
    }

    for old_word, new_word in replacements.items():
        question = question.replace(old_word, new_word)

    return question


def detect_crop(question):
    if "gandum" in question:
        return "Gandum"
    elif "chawal" in question:
        return "Chawal"
    elif "kapas" in question:
        return "Kapas"
    elif "makai" in question:
        return "Makai"
    elif "jowar" in question:
        return "Jowar"
    elif "til" in question:
        return "Til"
    else:
        return "Maloom nahi"


def detect_question_type(question):
    if "pani" in question:
        return "Pani"
    elif "khaad" in question:
        return "Khaad"
    elif "bimari" in question:
        return "Bimari"
    else:
        return "Maloom nahi"


def get_advice(crop, question_type):
    if crop == "Gandum" and question_type == "Pani":
        return (
            "Gandum ko pani mitti ki halat dekh kar dein. "
            "Agar mitti zyada sookhi ho to pani dein."
        )

    elif crop == "Gandum" and question_type == "Khaad":
        return (
            "Gandum ke liye khaad mitti aur fasal ki zaroorat "
            "dekh kar deni chahiye."
        )

    elif crop == "Gandum" and question_type == "Bimari":
        return (
            "Agar Gandum mein bimari nazar aa rahi hai to "
            "pehle bimari ki nishaniyan check karein."
        )

    elif crop == "Chawal" and question_type == "Pani":
        return (
            "Chawal ko fasal ki zaroorat ke mutabiq pani dein. "
            "Zaroorat se zyada pani na dein."
        )

    elif crop == "Kapas" and question_type == "Pani":
        return (
            "Kapas ko zaroorat ke mutabiq pani dein aur "
            "mitti ko bohat zyada geela na rakhein."
        )

    elif crop == "Makai" and question_type == "Pani":
        return (
            "Makai ko waqt par pani dein. "
            "Mitti ko bohat zyada sookhne na dein."
        )

    elif crop == "Jowar" and question_type == "Pani":
        return (
            "Jowar ko fasal ki zaroorat ke mutabiq pani dein."
        )

    elif crop == "Til" and question_type == "Pani":
        return (
            "Til ko zaroorat ke mutabiq pani dein aur "
            "zyada pani se bachayein."
        )

    else:
        return "Is sawal ke liye maloomat abhi hamare paas nahi hai."


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

    question = normalize_question(question)

    if not question:
        return jsonify({
            "status": "error",
            "message": "Sawal zaroor likhein."
        }), 400

    crop = detect_crop(question)
    question_type = detect_question_type(question)
    answer = get_advice(crop, question_type)

    return jsonify({
        "status": "success",
        "sawal": question,
        "fasal": crop,
        "sawal_ka_type": question_type,
        "jawab": answer
    })


if __name__ == "__main__":
    app.run(debug=True)