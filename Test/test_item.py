from django.test import TestCase, Client
from StuffTracker.models import MyUser, Stuff


# <new branch> In a different file, write a system test that shows that
#   an item added to the list immediately shows up in the rendered response.
# Load the test database with records to support your test.

class AddItemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MyUser(name="user", password="pass")
        self.user.save()
        Stuff(name="cat", owner=self.user).save()

        session = self.client.session
        session["name"] = "user"
        session.save()

    def test_add_item(self):
        response = self.client.post("/things/", {"stuff": "dog"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Stuff.objects.filter(name="dog", owner=self.user).exists())
        self.assertIn("dog", response.context["things"])
        self.assertContains(response, "dog")
        self.assertCountEqual(response.context["things"], ["cat", "dog"])



