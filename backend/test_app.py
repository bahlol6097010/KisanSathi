import unittest

from backend.app import app
from backend.app import (
    calculate_spray_quantity,
    load_knowledge_base
)


class KisanSathiAPITestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            b"Kisan Sathi Backend is Working!",
            response.data
        )

    def test_status(self):
        response = self.client.get("/api/status")

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["status"],
            "success"
        )

    def test_valid_advice(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko pani kab dena hai?"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["status"],
            "success"
        )

        self.assertEqual(
            data["fasal"],
            "Gandum"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Pani"
        )

    def test_empty_request(self):
        response = self.client.post(
            "/api/advice",
            json={}
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_empty_question(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": ""
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_unknown_crop(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Mujhe fasal ke bare mein mashwara chahiye."
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Maloom nahi"
        )

    def test_gehoon_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gehoon ko paani kab dena hai?"
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Gandum"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Pani"
        )

    def test_cotton_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri cotton ko pani chahiye."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Kapas"
        )

    def test_maize_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri maize ko pani kab dena hai?"
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Makai"
        )

    def test_knowledge_base_api(self):
        response = self.client.get(
            "/api/knowledge-base"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["status"],
            "success"
        )

        self.assertIn(
            "knowledge_base",
            data
        )

    def test_gandum_pani_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Gandum ko pani kab dena hai?"
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Gandum"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Pani"
        )

        self.assertNotEqual(
            data["jawab"],
            "Is sawal ke liye maloomat abhi hamare paas nahi hai."
        )

    def test_gandum_khaad_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Gandum mein khaad ka mashwara dein."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Gandum"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Khaad"
        )

    def test_gandum_bimari_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Gandum ki bimari ke bare mein batayein."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["fasal"],
            "Gandum"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Bimari"
        )

    def test_spray_topic(self):
        knowledge = load_knowledge_base()

        gandum = None

        for crop in knowledge["crops"]:

            if crop["name"] == "Gandum":
                gandum = crop
                break

        self.assertIsNotNone(
            gandum
        )

        self.assertIn(
            "Spray",
            gandum["topics"]
        )

    def test_yellow_rust_detection(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko peeli kungi lagi hai."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["bimari"],
            "Yellow Rust"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Spray"
        )

    def test_yellow_rust_spray_recommendation(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai. Spray batayein."
            }
        )

        data = response.get_json()

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "spray",
            data
        )

        self.assertEqual(
            data["spray"]["problem"],
            "Yellow Rust / Peeli Kungi"
        )

        self.assertEqual(
            data["spray"][
                "dose_per_litre_water_ml"
            ],
            1
        )

    def test_brown_rust_detection(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko bhuri kungi lagi hai."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["bimari"],
            "Brown Rust"
        )

        self.assertEqual(
            data["sawal_ka_type"],
            "Spray"
        )

    def test_brown_rust_spray_recommendation(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko brown rust lagi hai. Spray batayein."
            }
        )

        data = response.get_json()

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "spray",
            data
        )

        self.assertEqual(
            data["spray"]["problem"],
            "Brown Rust / Bhuri Kungi"
        )

        self.assertEqual(
            data["spray"][
                "dose_per_litre_water_ml"
            ],
            1
        )

    def test_yellow_leaves_do_not_confirm_disease(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ke pattay peelay ho rahe hain."
            }
        )

        data = response.get_json()

        self.assertEqual(
            data["bimari"],
            "Maloom nahi"
        )

    def test_acres_are_accepted(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai. Spray batayein.",
                "acres": 5
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["zameen_acres"],
            5
        )

    def test_decimal_acres_are_accepted(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": 2.5
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertEqual(
            data["zameen_acres"],
            2.5
        )

    def test_invalid_acres_are_rejected(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": -2
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_non_numeric_acres_are_rejected(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": "five"
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_spray_calculation_waits_for_verified_water_rate(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": 5
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        self.assertIn(
            "spray_calculation",
            data
        )

        self.assertEqual(
            data["spray_calculation"]["status"],
            "pending"
        )

        self.assertNotIn(
            "total_spray_ml",
            data["spray_calculation"]
        )

    def test_calculation_function_with_verified_water_rate(self):
        spray = {
            "dose_per_litre_water_ml": 1,
            "water_per_acre_liters": None
        }

        result = calculate_spray_quantity(
            5,
            spray,
            water_per_acre_override=200
        )

        self.assertEqual(
            result["status"],
            "calculated"
        )

        self.assertEqual(
            result["total_water_liters"],
            1000
        )

        self.assertEqual(
            result["total_spray_ml"],
            1000
        )

    def test_api_calculation_with_explicit_water_rate(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": 5,
                "water_per_acre_liters": 200
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.get_json()

        calculation = data[
            "spray_calculation"
        ]

        self.assertEqual(
            calculation["status"],
            "calculated"
        )

        self.assertEqual(
            calculation["total_water_liters"],
            1000
        )

        self.assertEqual(
            calculation["total_spray_ml"],
            1000
        )

    def test_invalid_water_per_acre_is_rejected(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question":
                    "Meri gandum ko yellow rust lagi hai.",
                "acres": 5,
                "water_per_acre_liters": -100
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )


if __name__ == "__main__":
    unittest.main()