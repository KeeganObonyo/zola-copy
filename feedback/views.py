from rest_framework import generics

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from customer.models import (
    Customer,
    Subscription
)

from .models import FeedBack

from .serializers import FeedBackSerializer

class AddFeedBackAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            company  = Customer.objects.get(username=request.user)
            FeedaBack.objects.create(
                author_name=request.data['author_name'],
                callback=request.data['callback'],
                text_info=request.data['text_info'],
                rating=request.data['rating'],
                customer=company
            )
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FeedBackListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedBackSerializer

    def get_queryset(self, *args, **kwargs):
        if Customer.objects.get(username=request.user).subscription.isactive:
            queryset_list = FeedBack.objects.filter(
                company__username=self.request.user
                )
            return queryset_list
        else:
            queryset_list = FeedBack.objects.filter(
                company__username=None
                )
            return queryset_list