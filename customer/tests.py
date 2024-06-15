from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APITestCase

from .views import (
    CustomerCreateAPIView,
    CustomerListView,
    CustomerProfileView,
    AddEmployees,
    EmployeeDeleteAPIView
)
from .models import (
    Customer,
    Employee,
    Subscription
)
from .serializers import (
    CustomerSerializer,
    CustomerCreateSerializer,
    EmployeeSerializer,
    SubscriptionSerializer
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
            password     = make_password(data['password'])
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

class CustomerTest(APITestCase):

    def setUp(self):
        me = SetUpMd()
        me.setUp()

    def test_CustomerCreateAPIView(self):
        url = reverse("register_new_customer")
        data = {
                "username": "Tester2",
                "first_name": "test",
                "last_name": "testy",
                "password": "password",
                "email": "zola@zola.reviews",
                "company_name":"Kilimanjaro Restaurant",
                "phone_number":"0700"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.filter(
            username='Tester2').exists(), True)
        self.assertEqual(Subscription.objects.all().count(), 2)

    def test_CustomerListView(self):
        expected_data = [{
        'first_name': 'test', 
        'last_name': 'testy', 
        'username': 'Tester', 
        'company_name': 'Kilimanjaro Restaurant', 
        'phone_number': '0700', 
        'email': 'zola@zola.reviews', 
        'place_id': None}]
        url = reverse("list_customer")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, 200)
       
    def test_AddEmployees(self):
        url = reverse("add_employees")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        data = {
            "employees":[{"username":"Employee1"},{"username":"Employee2"},{"username":"Employee3"}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Employee.objects.all().count(), 6)
 
    def test_EmployeeDeleteAPIView(self):
        url = reverse("delete_employees", args=['User3'])
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Employee.objects.all().count(), 2)

    def test_CustomerProfileView(self):
        expected_data = [{'first_name': 'test',
         'last_name': 'testy', 
         'username': 'Tester', 
         'company_name': 'Kilimanjaro Restaurant', 
         'phone_number': '0700', 
         'email': 'zola@zola.reviews', 
         'place_id': None}, 
         {'username': 'User1', 
         'company_name': None, 
         'phone_number': None, 
         'place_id': None}, 
         {'username': 'User2', 
         'company_name': None, 
         'phone_number': None, 
         'place_id': None}, 
         {'username': 'User3', 
         'company_name': None, 
         'phone_number': None, 
         'place_id': None}]
        url = reverse("customer_profile")
        self.client.credentials(
            HTTP_AUTHORIZATION=token_retrieve(self))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
