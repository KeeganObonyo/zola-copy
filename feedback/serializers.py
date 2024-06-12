from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import FeedBack

class FeedBackSerializer(ModelSerializer):

    class Meta:
        model = FeedBack
        fields = [
            'author_name'
            'callback'
            'text_info'
            'rating'
            'insertion_time'
            'company'
        ]
