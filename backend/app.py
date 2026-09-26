from flask import Flask, jsonify, request
import json
import os

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


def load_knowledge_base():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "knowledge_base.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


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
    elif "growth" in question:
        return "Growth"
    else:
        return "Maloom nahi"


def get_knowledge(crop, question_type):
    knowledge = load_knowledge_base()

    for crop_data in knowledge["crops"]:
        if crop_data["name"] == crop:
            topics = crop_data["topics"]

            if question_type in topics:
                information = topics[question_type]

                if information:
                    return information

    return []


@app.route("/api/knowledge-base", methods=["GET"])
def knowledge_base():
    try:
        knowledge = load_knowledge_base()

        return jsonify({
            "status": "success",
            "knowledge_base": knowledge
        })

    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "Knowledge Base file nahi mili."
        }), 500

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "Knowledge Base JSON file mein error hai."
        }), 500


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

    knowledge = get_knowledge(crop, question_type)

    if knowledge:
        answer = knowledge[0]["information"]
        source = knowledge[0]["source"]
    else:
        answer = "Is sawal ke liye maloomat abhi hamare paas nahi hai."
        source = "Knowledge Base mein maloomat available nahi."

    return jsonify({
        "status": "success",
        "sawal": question,
        "fasal": crop,
        "sawal_ka_type": question_type,
        "jawab": answer,
        "source": source
    })


if __name__ == "__main__":
    app.run(debug=True)