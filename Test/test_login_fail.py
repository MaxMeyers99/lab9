from django.test import TestCase, Client
from StuffTracker.models import MyUser, Stuff

# <new branch> In a different file, write a system test using Client that makes
#   sure on an unsuccessful login, the home page is redisplayed with a message.
# Load the test database with records to support your test.

class LoginFailTest(TestCase):

    def setUp(self):
        self.client = Client()
        user1 = MyUser(name="user1", password="pass1")
        user1.save()
        user2 = MyUser(name="user2", password="pass2")
        user2.save()
        Stuff(name="cat", owner=user1).save()
        Stuff(name="dog", owner=user1).save()
        Stuff(name="spoon", owner=user2).save()
        Stuff(name="fork", owner=user2).save()

    def test_wrong_pass(self):
        response = self.client.post("/", {"name": "user1", "password": "wrong"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "bad password")
        self.assertContains(response, "Home Page")
        self.assertContains(response, "bad password")
        self.assertNotIn("name", self.client.session)

    def test_other_user_pass(self):
        response = self.client.post("/", {"name": "user1", "password": "pass2"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "bad password")
        self.assertContains(response, "Home Page")
        self.assertNotIn("name", self.client.session)

    def test_empty_pass(self):
        response = self.client.post("/", {"name": "user1", "password": ""}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "bad password")
        self.assertContains(response, "Home Page")

    def test_new_user(self):
        response = self.client.post("/", {"name": "user3", "password": "pass3"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(MyUser.objects.filter(name="user3").exists())
        self.assertEqual(response.context["name"], "user3")
        self.assertNotContains(response, "dog")
        self.assertNotContains(response, "cat")
        self.assertNotContains(response, "spoon")
        self.assertNotContains(response, "fork")
        self.assertNotContains(response, "bad password")
        self.assertNotContains(response, "Home Page")


