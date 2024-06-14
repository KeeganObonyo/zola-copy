import requests

import zola_user.settings as st

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from customer.models import Customer


class RetrieveGooglePLaceId:
    def get_place_id(company_name):
        place_id_url   = st.GOOGLE_PLACES_API_URL
        google_api_key = st.GOOGLE_PLACES_API_KEY
        try:
            response = requests.get(place_id_url + "?fields=&input=" + company_name + "&inputtype=textquery&key=" + google_api_key)
            data = response.json()
            place_id  = data["candidates"][0]["place_id"]
            return place_id
        except:
            return None

class RetrieveGoogleReviewsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        place_detail_url   = st.GOOGLE_PLACES_API_DETAIL_URL
        google_api_key = st.GOOGLE_PLACES_API_KEY
        place_id = Customer.objects.get(username=request.user).place_id
        if Customer.objects.get(username=request.user).subscription.isactive:
            try:
                response = requests.get(place_detail_url + "?fields=name%2Crating%2Creviews&reviews_sort=newest&" + "place_id=" + place_id +"&key=" + google_api_key)
                data = response.json()
                reviews  = data["result"]["reviews"]
                return Response(data=reviews, status=status.HTTP_200_OK)
            except:
                raise Http404
        else:
            return Response(data="Dormant Account: Activate to Proceed",
                                status=status.HTTP_400_BAD_REQUEST)