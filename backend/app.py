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
    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    file_path = os.path.join(
        base_dir,
        "data",
        "knowledge_base.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
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
        "rice": "chawal",

        "kapas": "kapas",
        "cotton": "kapas",

        "makai": "makai",
        "maize": "makai",

        "jowar": "jowar",
        "sorghum": "jowar",

        "til": "til",
        "sesame": "til",

        "peeli kungi": "yellow rust",
        "peeli kungee": "yellow rust",
        "yellow rust": "yellow rust",

        "bhuri kungi": "brown rust",
        "bhuri kungee": "brown rust",
        "brown rust": "brown rust"
    }

    for old_word, new_word in replacements.items():
        question = question.replace(
            old_word,
            new_word
        )

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

    elif "spray" in question:
        return "Spray"

    elif "dawai" in question:
        return "Spray"

    elif "fungicide" in question:
        return "Spray"

    elif "yellow rust" in question:
        return "Spray"

    elif "brown rust" in question:
        return "Spray"

    elif "rust" in question:
        return "Spray"

    elif "kungi" in question:
        return "Spray"

    elif "bimari" in question:
        return "Bimari"

    elif "growth" in question:
        return "Growth"

    else:
        return "Maloom nahi"


def detect_disease(question):

    if "yellow rust" in question:
        return "Yellow Rust"

    elif "brown rust" in question:
        return "Brown Rust"

    elif "smut" in question:
        return "Smut"

    else:
        return "Maloom nahi"


def get_knowledge(
    crop,
    question_type
):

    knowledge = load_knowledge_base()

    for crop_data in knowledge["crops"]:

        if crop_data["name"] != crop:
            continue

        topics = crop_data["topics"]

        if question_type in topics:

            information = topics[
                question_type
            ]

            if information:
                return information

    return []


def get_spray_recommendation(
    crop,
    disease
):

    knowledge = load_knowledge_base()

    for crop_data in knowledge["crops"]:

        if crop_data["name"] != crop:
            continue

        spray_data = crop_data[
            "topics"
        ].get(
            "Spray",
            []
        )

        for spray in spray_data:

            problem = spray.get(
                "problem",
                ""
            ).lower()

            if disease == "Yellow Rust":

                if "yellow rust" in problem:
                    return spray

            elif disease == "Brown Rust":

                if "brown rust" in problem:
                    return spray

    return None


def validate_acres(value):

    if value is None:
        return None, None

    try:
        acres = float(value)

    except (TypeError, ValueError):

        return None, (
            "Zameen acres mein number honi chahiye."
        )

    if acres <= 0:

        return None, (
            "Zameen 0 se zyada honi chahiye."
        )

    return acres, None


def validate_water_per_acre(value):

    if value is None:
        return None, None

    try:
        water = float(value)

    except (TypeError, ValueError):

        return None, (
            "Water per acre litres mein "
            "number honi chahiye."
        )

    if water <= 0:

        return None, (
            "Water per acre 0 se zyada "
            "honi chahiye."
        )

    return water, None


def calculate_spray_quantity(
    acres,
    spray,
    water_per_acre_override=None
):

    if acres is None:
        return None

    if spray is None:
        return None

    dose_per_litre = spray.get(
        "dose_per_litre_water_ml"
    )

    if dose_per_litre is None:

        return {
            "status": "pending",
            "message": (
                "Is spray ki dose per litre "
                "Knowledge Base mein available "
                "nahi hai."
            )
        }

    if water_per_acre_override is not None:

        water_per_acre = (
            water_per_acre_override
        )

    else:

        water_per_acre = spray.get(
            "water_per_acre_liters"
        )

    if water_per_acre is None:

        return {
            "status": "pending",
            "message": (
                "Total spray quantity calculate "
                "karne ke liye Pakistan-specific "
                "verified water-per-acre rate "
                "abhi Knowledge Base mein "
                "available nahi hai."
            ),
            "dose_per_litre_water_ml": (
                dose_per_litre
            )
        }

    total_water = (
        acres * water_per_acre
    )

    total_spray = (
        total_water * dose_per_litre
    )

    spray_per_acre = (
        water_per_acre * dose_per_litre
    )

    return {
        "status": "calculated",
        "acres": acres,
        "water_per_acre_liters": (
            water_per_acre
        ),
        "total_water_liters": round(
            total_water,
            2
        ),
        "dose_per_litre_water_ml": (
            dose_per_litre
        ),
        "spray_per_acre_ml": round(
            spray_per_acre,
            2
        ),
        "total_spray_ml": round(
            total_spray,
            2
        )
    }


@app.route(
    "/api/knowledge-base",
    methods=["GET"]
)
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
            "message": (
                "Knowledge Base file nahi mili."
            )
        }), 500

    except json.JSONDecodeError:

        return jsonify({
            "status": "error",
            "message": (
                "Knowledge Base JSON file mein "
                "error hai."
            )
        }), 500


@app.route(
    "/api/advice",
    methods=["POST"]
)
def advice():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Sawal bhejein."
        }), 400

    question = data.get(
        "question"
    )

    if not question:

        return jsonify({
            "status": "error",
            "message": (
                "Sawal zaroor likhein."
            )
        }), 400

    question = normalize_question(
        question
    )

    if not question:

        return jsonify({
            "status": "error",
            "message": (
                "Sawal zaroor likhein."
            )
        }), 400

    acres, acres_error = (
        validate_acres(
            data.get("acres")
        )
    )

    if acres_error:

        return jsonify({
            "status": "error",
            "message": acres_error
        }), 400

    water_per_acre, water_error = (
        validate_water_per_acre(
            data.get(
                "water_per_acre_liters"
            )
        )
    )

    if water_error:

        return jsonify({
            "status": "error",
            "message": water_error
        }), 400

    crop = detect_crop(
        question
    )

    question_type = (
        detect_question_type(
            question
        )
    )

    disease = detect_disease(
        question
    )

    spray_recommendation = None

    if disease != "Maloom nahi":

        spray_recommendation = (
            get_spray_recommendation(
                crop,
                disease
            )
        )

    if spray_recommendation:

        answer = (
            spray_recommendation[
                "information"
            ]
        )

        source = (
            spray_recommendation[
                "source"
            ]
        )

    else:

        knowledge = get_knowledge(
            crop,
            question_type
        )

        if knowledge:

            answer = (
                knowledge[0][
                    "information"
                ]
            )

            source = (
                knowledge[0][
                    "source"
                ]
            )

        elif disease != "Maloom nahi":

            answer = (
                "Bimari identify ho gayi hai, "
                "lekin is bimari ke liye spray "
                "information abhi Knowledge Base "
                "mein available nahi hai."
            )

            source = (
                "Knowledge Base mein spray "
                "recommendation available nahi."
            )

        else:

            answer = (
                "Is sawal ke liye maloomat "
                "abhi hamare paas nahi hai."
            )

            source = (
                "Knowledge Base mein maloomat "
                "available nahi."
            )

    response_data = {
        "status": "success",
        "sawal": question,
        "fasal": crop,
        "sawal_ka_type": question_type,
        "bimari": disease,
        "jawab": answer,
        "source": source
    }

    if acres is not None:

        response_data[
            "zameen_acres"
        ] = acres

    if spray_recommendation:

        response_data["spray"] = {

            "problem": (
                spray_recommendation[
                    "problem"
                ]
            ),

            "information": (
                spray_recommendation[
                    "information"
                ]
            ),

            "source": (
                spray_recommendation[
                    "source"
                ]
            ),

            "dose_per_litre_water_ml": (
                spray_recommendation.get(
                    "dose_per_litre_water_ml"
                )
            ),

            "water_per_acre_liters": (
                spray_recommendation.get(
                    "water_per_acre_liters"
                )
            ),

            "water_rate_status": (
                spray_recommendation.get(
                    "water_rate_status"
                )
            )
        }

        if acres is not None:

            calculation = (
                calculate_spray_quantity(
                    acres,
                    spray_recommendation,
                    water_per_acre
                )
            )

            response_data[
                "spray_calculation"
            ] = calculation

    return jsonify(
        response_data
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )