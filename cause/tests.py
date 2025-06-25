import json
import uuid
from django.test import TestCase
from rest_framework.test import APIClient

from cause.models import Cause, Donation


class CauseAPITestCase(TestCase):
    """POST(create) test case"""

    client = APIClient()

    DATA = {
        "title": "Healing Through Hope",
        "description": "For mental health or disaster relief",
        "image_url": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449",
    }

    def test_cause_can_be_created(self):

        response = self.client.post("/api/v1/causes/", self.DATA, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Cause.objects.filter(title=self.DATA.get("title")).exists()
        )

    def test_missing_fields_raise_400_exception(self):

        fields = self.DATA.keys()

        for field in fields:

            # clone the data
            data = dict(self.DATA)
            data.pop(field)  # remove a field

            response = self.client.post("/api/v1/causes/", data, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertFalse(
                Cause.objects.filter(title=data.get("title")).exists()
            )

    def test_cause_titles_are_unique(self):

        response = self.client.post("/api/v1/causes/", self.DATA, format="json")
        self.assertEqual(response.status_code, 201)

        data = dict(self.DATA)
        data["description"] = "Another charity for children"
        data["image_url"] = (
            "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449"
        )

        response = self.client.post("/api/v1/causes/", self.DATA, format="json")
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            Cause.objects.filter(title=self.DATA.get("title")).count(), 1
        )

    def test_image_url_is_validated(self):

        data = dict(self.DATA)
        data["image_url"] = "http//image"

        response = self.client.post("/api/v1/causes/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Cause.objects.filter(title=data.get("title")).exists())


class CauseTestCase(TestCase):
    """PUT (update)/ GET (retreive and list) / DELETE / POST (contribution) test cases"""

    client = APIClient()
    uid = "798e09a9-3d97-4980-aa86-a49e20a9d4c4"

    def setUp(self) -> None:
        """Seeds the db with cause entities"""

        causes = [
            Cause(
                id=self.uid,
                title="Clean Hands, Bright Futures",
                description="Education on hygiene and health",
                image_url="https://www.google.com/url",
            ),
            Cause(
                title="Steps for Shelter",
                description="For homelessness awareness",
                image_url="https://home.com",
            ),
            Cause(
                title="For mental health or disaster relief",
                description="For mental health or disaster relief",
                image_url="https://health.com",
            ),
        ]

        Cause.objects.bulk_create(causes)

    def test_can_fetch_all_causes(self):

        response = self.client.get("/api/v1/causes/", format="json")
        self.assertEqual(response.status_code, 200)

        causes = response.json().get("data")
        self.assertEqual(len(causes), 3)

    def test_can_retrieve_a_cause(self):

        response = self.client.get(f"/api/v1/causes/{self.uid}/", format="json")
        self.assertEqual(response.status_code, 200)

        cause = response.json()
        cause = cause.get("data")

        self.assertEqual(cause.get("id"), self.uid)
        self.assertEqual(cause.get("title"), "Clean Hands, Bright Futures")
        self.assertEqual(
            cause.get("description"), "Education on hygiene and health"
        )
        self.assertEqual(cause.get("image_url"), "https://www.google.com/url")

    def test_cause_can_be_updated(self):

        cause = Cause.objects.get(id=self.uid)

        data = {
            "title": cause.title,
            "description": "Another charity for children",
            "image_url": cause.image_url,
        }
        response = self.client.put(
            f"/api/v1/causes/{self.uid}/",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        cause.refresh_from_db()
        self.assertEqual(cause.description, "Another charity for children")

    def test_contribution_can_be_added_to_cause(self):

        cause = Cause.objects.get(id=self.uid)
        contribution = {
            "name": "Sarki Abdul",
            "email": "sarkiihima44@gmail.com",
            "amount": 10.33,
        }

        response = self.client.post(
            f"/api/v1/causes/{self.uid}/contribute/",
            contribution,
            format="json",
        )

        cause.refresh_from_db()
        self.assertEqual(response.status_code, 201)

        self.assertTrue(Donation.objects.filter(**contribution).exists())
        self.assertTrue(cause.donations.filter(**contribution).exists())

    def test_can_delete_a_cause(self):

        response = self.client.delete(
            f"/api/v1/causes/{self.uid}/", format="json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Cause.objects.filter(id=self.uid).exists())
