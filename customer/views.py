from django.http import Http404

from rest_framework import generics
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import (
    DestroyModelMixin,
    UpdateModelMixin)
from .models import ( Customer, Employee)
from .serializers import (
    CustomerCreateSerializer,
    CustomerSerializer,
    EmployeeSerializer
)

from itertools import chain

class CustomerCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny,]
    serializer_class   = CustomerCreateSerializer
    queryset           = Customer.objects.all()

class CustomerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset         = Customer.objects.all()

class CustomerProfileView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Employee.objects.filter(
            company__username=self.request.user
            )
        customer_profile = Customer.objects.filter(username=self.request.user)
        return chain(customer_profile, queryset_list)

class AddEmployees(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset           = Employee.objects.all()

    def post(self, request, format=None):
        if Customer.objects.get(username=request.user).subscription.isactive:
            try:
                employees = request.data['employees']
                for item in employees:
                    company  = Customer.objects.get(username=request.user)
                    username = item['username']
                    try:
                        Employee.objects.get(
                        username = username,
                        company = company
                        )
                    except:
                        employee = Employee.objects.create(
                            username = username,
                            company  = company
                        )
                return Response(data="Employees added successfully", status=status.HTTP_200_OK)
            except:
                return Response(data="No employee list provided",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Dormant Account: Activate to Proceed",
                                status=status.HTTP_400_BAD_REQUEST)

class EmployeeDeleteAPIView(APIView):
    queryset = Employee.objects.all()

    def get(self, request, username, format=None):
        if Customer.objects.get(username=request.user).subscription.isactive:
            try:
                employee = Employee.objects.get(username=username).delete()
            except:
                raise Http404
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="Dormant Account: Activate to Proceed",
                                status=status.HTTP_400_BAD_REQUEST)
