from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIRequestFactory, APITestCase

from .views import *
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

    def test_RetrieveGoogleReviewsAPIView(self):
        url = reverse("retrirve_reviews")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        expected_data = [{'author_name': 'Adan Ahmed', 
        'author_url': 'https://www.google.com/maps/contrib/104957897105311865387/reviews', 
        'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjUC6abtqH2lMHnRWgbSCbuIjqxmAgtpMJSz_IJFvkcYi3c7YMsl=s128-c0x00000000-cc-rp-mo-ba3', 
        'rating': 5, 
        'relative_time_description': 'a week ago', 
        'text': '', 
        'time': 1717444149, 
        'translated': False}, 
        {'author_name': 'Adan Abdi (Adesh)', 
        'author_url': 'https://www.google.com/maps/contrib/115457450912541221206/reviews', 
        'language': 'en', 
        'original_language': 'en', 
        'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjWSozf3QCjz2I2RemxmuZjOKo4o3XR1FrDoRmIqSSigmUcBsaTm=s128-c0x00000000-cc-rp-mo-ba4', 
        'rating': 5, 
        'relative_time_description': '2 weeks ago', 
        'text': 'I love the food here, my take was pilau goes for Ksh 500. Price was fair', 
        'time': 1716808545, 'translated': False}, {'author_name': 'Karume Robert', 
        'author_url': 'https://www.google.com/maps/contrib/106540546263532359878/reviews', 
        'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjUcqBi1n2WCYbzjIY15BccYgobuiw6MWUpS4xUEEWxngCB4bSY=s128-c0x00000000-cc-rp-mo-ba3', 
        'rating': 5, 
        'relative_time_description': 'a month ago', 
        'text': '', 
        'time': 1714732263, 
        'translated': False}, 
        {'author_name': 'Abdinasir Haji', 
        'author_url': 'https://www.google.com/maps/contrib/102706284029389220219/reviews', 
        'profile_photo_url': 'https://lh3.googleusercontent.com/a/ACg8ocKhZZCp4eapbQphlOAxyNRCXyD3R2qLaSzCAc0CsN21AAmrgns=s128-c0x00000000-cc-rp-mo', 
        'rating': 5, 
        'relative_time_description': 'a month ago', 
        'text': '', 
        'time': 1714211277, 
        'translated': False}, 
        {'author_name': 'Abdinasir Mohamed 4379', 
        'author_url': 'https://www.google.com/maps/contrib/110104440451885385948/reviews', 
        'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjWwiHNddP36Pff7VFc6wRqVWf3C0VRjvS-3wG_tf3qY1DtrZLVM=s128-c0x00000000-cc-rp-mo', 
        'rating': 5, 
        'relative_time_description': '2 months ago', 
        'text': '', 
        'time': 1713128849, 
        'translated': False}]
        self.assertEqual(response.data, expected_data)