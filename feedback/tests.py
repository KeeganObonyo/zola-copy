from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase

from .views import (
    AddFeedBackAPIView,
    FeedBackListView
)
from .models import FeedBack

from customer.models import (
    Customer,
    Subscription,
    Employee
)

from review.views import RetrieveGooglePLaceId

def token_retrieve(self):
    login_cred = {
        "username": "Tester",
        "password": "password"
    }
    url = reverse('obtain_token')
    response = self.client.post(url, login_cred, format='json')
    token = "Bearer " + response.data["access"]
    return token


class SetUpMd(APITestCase):

    @classmethod
    def setUp(cls):
        data = {
                "username": "Tester",
                "first_name": "test",
                "last_name": "testy",
                "password": "password",
                "email": "zola@zola.reviews",
                "company_name":"Kilimanjaro Restaurant",
                "phone_number":"0700"
            }

        user1 = Customer.objects.create(
            first_name   = data['first_name'],
            last_name    = data['last_name'],
            username     = data['username'],
            phone_number = data['phone_number'],
            company_name = data['company_name'],
            email        = data['email'],
            password     = make_password(data['password']),
            place_id     = "ChIJdbRVtrQWLxgRNV68z2IR5tw"
        )

        subscription1 = Subscription.objects.create(
            isactive = True,
            company  = user1
        )

        employee1 = Employee.objects.create(
            username = "User1",
            company  = user1
        )

        employee2 = Employee.objects.create(
            username = "User2",
            company  = user1
        )

        employee3 = Employee.objects.create(
            username = "User3",
            company  = user1
        )

        feedback1 = FeedBack.objects.create(
            author_name = "Zola",
            callback    = "0700",
            text_info   = "Awesomeness",
            rating      = 5,
            employee    = "Dragon",
            company     = user1
        )

class ReviewTest(APITestCase):

    def setUp(self):
        me = SetUpMd()
        me.setUp()

    def test_AddFeedBackAPIView(self):
        url = reverse("add_feedback")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        data = {
                "author_name":"Zola",
                "callback":"0700",
                "text_info":"Awesomeness",
                "rating":5,
                "employee":"Dragon",
                "username":"Tester"
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Feedback added successfully")
        self.assertEqual(FeedBack.objects.all().count(), 2)

    def test_FeedBackListView(self):
        url = reverse("list_feedback")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)