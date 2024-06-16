from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase

from .views import (
    RetrieveGooglePLaceId,
    RetrieveGoogleReviewsAPIView
)
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

class ReviewTest(APITestCase):

    def setUp(self):
        me = SetUpMd()
        me.setUp()

    def test_RetrieveGooglePLaceId(self):
        place_id = RetrieveGooglePLaceId.get_place_id("Kilimanjaro Restaurant")
        assert(place_id != None)

        url = reverse("retrieve_place_id", args=['Tester'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        assert(response.data != None)

    def test_RetrieveGoogleReviewsAPIView(self):
        url = reverse("retrieve_reviews")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        assert(response.data != None)