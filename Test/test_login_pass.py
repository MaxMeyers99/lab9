from django.test import TestCase, Client
from StuffTracker.models import MyUser, Stuff

# Write a system test using Client that makes sure that on a successful
#   login the correct user's item list is displayed.
# Load the test database with records to support your test. <done>

class LoginPassTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = MyUser(name="user1", password="pass1")
        user1.save()
        user2 = MyUser(name="user2", password="pass2")
        user2.save()
        Stuff(name="cat", owner=user1).save()
        Stuff(name="dog", owner=user1).save()
        Stuff(name="spoon", owner=user2).save()

    def test_correct_items_after_login(self):
        response = self.client.post("/", {"name": "user1", "password": "pass1"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["name"], "user1")
        self.assertEqual(self.client.session["name"], "user1")
        self.assertCountEqual(response.context["things"], ["cat", "dog"])
        self.assertContains(response, "cat")
        self.assertContains(response, "dog")
        self.assertNotContains(response, "spoon")
