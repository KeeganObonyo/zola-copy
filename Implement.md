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

[
    {
        "author_name": "Adan Ahmed",
        "author_url": "https://www.google.com/maps/contrib/104957897105311865387/reviews",
        "profile_photo_url": "https://lh3.googleusercontent.com/a-/ALV-UjUC6abtqH2lMHnRWgbSCbuIjqxmAgtpMJSz_IJFvkcYi3c7YMsl=s128-c0x00000000-cc-rp-mo-ba3",
        "rating": 5,
        "relative_time_description": "a week ago",
        "text": "",
        "time": 1717444149,
        "translated": false
    },
    {
        "author_name": "Adan Abdi (Adesh)",
        "author_url": "https://www.google.com/maps/contrib/115457450912541221206/reviews",
        "language": "en",
        "original_language": "en",
        "profile_photo_url": "https://lh3.googleusercontent.com/a-/ALV-UjWSozf3QCjz2I2RemxmuZjOKo4o3XR1FrDoRmIqSSigmUcBsaTm=s128-c0x00000000-cc-rp-mo-ba4",
        "rating": 5,
        "relative_time_description": "2 weeks ago",
        "text": "I love the food here, my take was pilau goes for Ksh 500. Price was fair",
        "time": 1716808545,
        "translated": false
    },
    {
        "author_name": "Karume Robert",
        "author_url": "https://www.google.com/maps/contrib/106540546263532359878/reviews",
        "profile_photo_url": "https://lh3.googleusercontent.com/a-/ALV-UjUcqBi1n2WCYbzjIY15BccYgobuiw6MWUpS4xUEEWxngCB4bSY=s128-c0x00000000-cc-rp-mo-ba3",
        "rating": 5,
        "relative_time_description": "a month ago",
        "text": "",
        "time": 1714732263,
        "translated": false
    },
    {
        "author_name": "Abdinasir Haji",
        "author_url": "https://www.google.com/maps/contrib/102706284029389220219/reviews",
        "profile_photo_url": "https://lh3.googleusercontent.com/a/ACg8ocKhZZCp4eapbQphlOAxyNRCXyD3R2qLaSzCAc0CsN21AAmrgns=s128-c0x00000000-cc-rp-mo",
        "rating": 5,
        "relative_time_description": "a month ago",
        "text": "",
        "time": 1714211277,
        "translated": false
    },
    {
        "author_name": "Abdinasir Mohamed 4379",
        "author_url": "https://www.google.com/maps/contrib/110104440451885385948/reviews",
        "profile_photo_url": "https://lh3.googleusercontent.com/a-/ALV-UjWwiHNddP36Pff7VFc6wRqVWf3C0VRjvS-3wG_tf3qY1DtrZLVM=s128-c0x00000000-cc-rp-mo",
        "rating": 5,
        "relative_time_description": "a month ago",
        "text": "",
        "time": 1713128849,
        "translated": false
    }
]

You don't have to consume the extra fields but I figure they are a nice to have.

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
