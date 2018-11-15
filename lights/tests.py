from django.test import TestCase

from .models import Color


class LightsTest(TestCase):
    def test_no_color(self):
        self.assertRaises(Color.DoesNotExist, Color.objects.get)
        resp = self.client.get("/lights/LEDP.txt")
        self.assertEqual(resp["content-type"], "text/plain")
        self.assertEqual(resp.content, b"255\n0\n0")

    def test_set_color(self):
        resp = self.client.post("/lights/submit", {"R": 100, "G": 100, "B": 100})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get("/lights/LEDP.txt")
        self.assertEqual(resp["content-type"], "text/plain")
        self.assertEqual(resp.content, b"100\n100\n100")

        resp = self.client.post("/lights/submit", {"R": 111, "G": 111, "B": 111})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get("/lights/LEDP.txt")
        self.assertEqual(resp["content-type"], "text/plain")
        self.assertEqual(resp.content, b"111\n111\n111")

    def test_template(self):
        resp = self.client.get("/lights/")
        self.assertTemplateUsed(resp, "lights/index.html")
