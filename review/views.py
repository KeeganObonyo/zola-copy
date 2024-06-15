import requests

import zola_api.settings as st

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
            response = requests.get(place_id_url + 
            "?fields=&input=" + company_name + 
            "&inputtype=textquery&key=" + google_api_key
            )
            data = response.json()
            place_id  = data["candidates"][0]["place_id"]
            return place_id
        except:
            return None

class RetrieveGoogleReviewsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        out_scraper_url          = st.OUT_SCRAPER_URL
        out_scraper_api_key      = st.OUT_SCRAPER_API_KEY
        out_scraper_review_limit = st.OUT_SCRAPER_REVIEW_LIMIT

        place_id = Customer.objects.get(username=request.user).place_id

        if Customer.objects.get(username=request.user).subscription.isactive:
            try:
                response = requests.get(out_scraper_url + 
                "query=" + place_id + 
                "&reviewsLimit=" + out_scraper_review_limit + "&async=false",
                headers={"X-API-KEY": out_scraper_api_key}
                )
                data = response.json()["data"][0]

                review_data = {}
                review_data["rating"]=data["rating"]
                review_data["reviews"]=data["reviews"]

                reviews_list=list()
                for item in data["reviews_data"]:
                    review = {}
                    review["author_name"]=item["author_title"]
                    review["text"]=item["review_text"]
                    review["rating"]=item["review_rating"]
                    review["date"]=item["review_datetime_utc"]
                    reviews_list.append(review)

                review_data["reviews_list"] = reviews_list
                return Response(data=review_data, status=status.HTTP_200_OK)
            except:
                raise Http404
        else:
            return Response(data="Dormant Account: Activate to Proceed",
                                status=status.HTTP_400_BAD_REQUEST)