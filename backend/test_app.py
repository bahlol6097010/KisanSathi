import unittest

from backend.app import app


class TestKisanSathiAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Kisan Sathi Backend is Working!",
            response.get_data(as_text=True)
        )

    def test_status(self):
        response = self.client.get("/api/status")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "success")
        self.assertIn("running", data["message"])

    def test_valid_advice(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Meri gandum ko pani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["fasal"], "Gandum")
        self.assertEqual(data["sawal_ka_type"], "Pani")

    def test_empty_request(self):
        response = self.client.post(
            "/api/advice",
            json={}
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertEqual(data["status"], "error")
        self.assertEqual(data["message"], "Sawal bhejein.")

    def test_empty_question(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "   "
            }
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()

        self.assertEqual(data["status"], "error")
        self.assertEqual(data["message"], "Sawal zaroor likhein.")

    def test_unknown_crop(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Meri fasal ko pani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["fasal"], "Maloom nahi")

    def test_gehoon_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Meri gehoon ko paani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Gandum")
        self.assertEqual(data["sawal_ka_type"], "Pani")

    def test_cotton_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Cotton ko pani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Kapas")

    def test_maize_normalization(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Maize ko pani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Makai")

    def test_knowledge_base_api(self):
        response = self.client.get("/api/knowledge-base")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "success")
        self.assertIn("knowledge_base", data)

    def test_gandum_pani_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Meri gandum ko pani kab dena hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Gandum")
        self.assertEqual(data["sawal_ka_type"], "Pani")
        self.assertNotEqual(data["jawab"], "")
        self.assertNotEqual(data["source"], "")

    def test_gandum_khaad_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Gandum ke liye khaad ka kya mashwara hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Gandum")
        self.assertEqual(data["sawal_ka_type"], "Khaad")
        self.assertNotEqual(data["jawab"], "")
        self.assertNotEqual(data["source"], "")

    def test_gandum_bimari_knowledge(self):
        response = self.client.post(
            "/api/advice",
            json={
                "question": "Gandum mein bimari ka kya mashwara hai?"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["fasal"], "Gandum")
        self.assertEqual(data["sawal_ka_type"], "Bimari")
        self.assertNotEqual(data["jawab"], "")
        self.assertNotEqual(data["source"], "")


if __name__ == "__main__":
    unittest.main(verbosity=2)