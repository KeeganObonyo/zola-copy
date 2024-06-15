from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from customer.views import (
    CustomerCreateAPIView, 
    CustomerListView,
    AddEmployees,
    EmployeeDeleteAPIView,
    CustomerProfileView
)

from review.views import (
    RetrieveGoogleReviewsAPIView
)

from feedback.views import (
    AddFeedBackAPIView,
    FeedBackListView
)

urlpatterns = [
    path('api/zola/register/', CustomerCreateAPIView.as_view(), name='register_new_customer'),
    path('api/zola/customer/list', CustomerListView.as_view(), name='list_customer'),
    path('api/zola/get_token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('api/zola/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/zola/profile', CustomerProfileView.as_view(), name='customer_profile'),
    path('api/zola/add_employees', AddEmployees.as_view(), name='add_employees'),
    path('api/zola/delete_employee/<str:username>', EmployeeDeleteAPIView.as_view(), name='delete_employees'),
    path('api/list/review', RetrieveGoogleReviewsAPIView.as_view(), name='retrirve_reviews'),
    path('api/add/feedback', AddFeedBackAPIView.as_view(), name='add_feedback'),
    path('api/list/feedback', FeedBackListView.as_view(), name='list_feedback'),
    path('admin/', admin.site.urls),
]
