#API Implementation Guide
Important update. When the user is registered we automatically get and store their place id. Couldn't do that previously as we were using firebase for authentication. P.S proof of concept. Moreover we get the details of the particular account on authentication hence no need to be sent for every request. Also their acount needs to be activated first before they can add employees or get info on their dashboard. Else they get the info: status 400. "Dormant Account: Activate to Proceed"

1. Register new user

uri: https://zola.technology/api/zola/register/

request type: POST
request body: {
    "first_name"="",
    "last_name"="",
    "username"="",
    "phone_number"="",
    "company_name"="",
    "email":"",
    "password":""
}

response: status 200

2. Authentication: We're using JWT for all requests to the API.

uri: https://zola.technology/api/zola/get_token/

request type: POST
request body: {
    "username":"",
    "password":""
}

response: status 200

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxODM1NTA2OSwiaWF0IjoxNzE4MjY4NjY5LCJqdGkiOiI4Y2E3Y2VkNzA1NDg0ZWIwYTdiZThkMWYxZTBmYjMxMyIsInVzZXJfaWQiOjV9.2k9f5cqG29I83oEPladaSQch2RrMZrr2_LBjh0lrREc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MzU1MDY5LCJpYXQiOjE3MTgyNjg2NjksImp0aSI6IjFkMWE5M2I4YzI3ODRkMWY5Mzc4MmUxZDA2NmRlMmViIiwidXNlcl9pZCI6NX0.PqoofyY2bBeVZBW_Fr9L4aPYib0A71Fy2W7WqbyX0Vg"
}

Use the corresponding response token for authentication. and '/api/zola/refresh_token/' endpoint to refresh the token.

3. Add employees to the user account/business.

uri: https://zola.technology/api/zola/add_employees

request type: POST
request body: {
    "employess":[{"username":""},{"username":""}]
}

response: status 200 "Employees added successfully"

4. Delete employees from the profile.

uri: https://zola.technology/api/zola/delete_employee/<str:username>

request type: GET

response: status 204

4. Get user profile.

uri: https://zola.technology/api/zola/profile

request type: GET

response: status 200

[
    {
        "first_name": "shiko",
        "last_name": "shaka",
        "username": "the_guy",
        "company_name": "0705417514",
        "phone_number": "0705417514",
        "email": "keegan@zola.reviews",
        "place_id": null
    },
    {
        "username": "keego",
        "company_name": null,
        "phone_number": null,
        "place_id": null
    },
    {
        "username": "bro",
        "company_name": null,
        "phone_number": null,
        "place_id": null
    }
]

It is a combined queryset with the first object as the user/company profile and the corresponding objects as the employees.

5. Get list of reviews from google.

uri: https://zola.technology/api/list/review

request type: GET

response: status 200

{
    "rating": 4.3,
    "reviews": 6094,
    "reviews_list": [
        {
            "author_name": "Esther Wamugunda",
            "text": "Kilimanjaro Restaurant is a bustling eatery, particularly during lunch hours, with plenty of attentive wait staff available to cater to the crowd. The menu offers Swahili-inspired dishes, including the biryani. However, I found the chicken in the biryani to be lacking freshness, which was disappointing.\n\nThe restaurant's flavors have undergone changes over time, with the once bold and vibrant tastes becoming less pronounced. While the bathrooms are clean, it's worth noting that the ladies' and gents' facilities are located separately. The portion sizes at Kilimanjaro are quite generous, often too much for a single person to consume, so sharing a dish is recommended.\n\nKilimanjaro Restaurant provides fast service, and the wait staff are helpful and attentive. They have an online ordering system in place, making it convenient for customers to place their orders by scanning the provided QR code.",
            "rating": 4,
            "date": "04/16/2024 17:30:30"
        },
        {
            "author_name": "Lawrence Raul",
            "text": "Had a dinner meeting at this place, and we found it amazing. Top-notch services from the waiter who served us, he was readily available for us, and he recommended the plater to us, which was good, and portion was large, but I felt it could have been better, I loved the arosto and guacamole, as it was nicely done. The passion was great. I couldn't get enough of it.  The outside setting was great as the ambiance was cool. Would recommend groups or couples.  The restaurant is Halal.",
            "rating": 4,
            "date": "04/05/2024 20:53:59"
        },
        {
            "author_name": "Gertrude Auma",
            "text": "Good food and service. Got one of their platters for a group of 6. Also got a cake and they did sing happy birthday. Overall nice place.",
            "rating": 3,
            "date": "04/07/2024 16:57:05"
        },
        {
            "author_name": "Samin Kashmy",
            "text": "The goat meat was nicely cooked. However, the overall taste of goat, chicken, pilao were bland for my South asian taste buds! While they provide you with Chilli sauce and ketchup, they should consider expanding to offer black pepper, and salt, catering to South asian people.\n\nWe went there on valentines day; hence, it was crazily crowded. However, we could manage a seat without prior reservation.\n\nThe server also didn't bring our kachumbari, which was with the platter. Probably they're ran out of it!",
            "rating": 4,
            "date": "02/16/2024 13:35:32"
        },
        {
            "author_name": "Rennis Napoleon",
            "text": "When you are in Nairobi town and you want to grab something to eat this is a nice place to go\nFair prices\nFood 7/10",
            "rating": 3,
            "date": "05/20/2024 02:55:31"
        }
    ]
}

It additionally contains info like total no of reviews and average rating.

6. Add feedback.
The feedback view doesn't require authentication as any one should be able to make a feedback. But if the account is innactive this featureis diabled.

uri: https://zola.technology/api/add/feedback

request type: POST

request body: {
    "author_name":"",
    "callback":"",
    "text_info":"",
    "rating":"",
    "employee":"",
    "username":""
}

response: status 200
"Feedback added successfully"

7. Get feedback list.

uri: https://zola.technology/api/list/feedback

request type: GET

response: status 200

[
    {
        "author_name": "mimi",
        "callback": "0705417514",
        "text_info": "stuff",
        "rating": 4,
        "insertion_time": "2024-06-13T10:11:44.212866Z",
        "company": 5
    },
    {
        "author_name": "mimi",
        "callback": "0705417514",
        "text_info": "stuff",
        "rating": 4,
        "insertion_time": "2024-06-13T10:12:35.271111Z",
        "company": 5
    }
]
