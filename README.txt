
To access token-access-only API endpoints, perform the following steps:
- obtain access token by submitting correct user login credentials to the login API endpoint: /login/
- authorization username is the email address
- Place the access token inside the HTTP Headers with "x-access-token" as the key and the token as the value.
- token expires in 3 hours


ENDPOINTS FOR LOGIN AUTHENTICATION

name: login()
endpoint: /login/
methods: GET
token required: no
note: make a GET request to the API endpoint with username and password in the HTTP Authorization header to get a token back as respose.



ENDPOINT FOR USERS

name: get_users()
endpoint: /users/
methods: GET
token required: no

name get_nearby_users()
endpoint: /users/nearby/<longitude>/<latitude>/<max_distance>/
methods: GET
token required: no

name: add_user()
endpoint: /user/create/
methods: POST
token required: yes
input JSON params: 

name: update_user()
endpoint: /user/update/
methods: PUT
token required: yes
input JSON params: 

name: get_user()
endpoint: /user/<user_id>/
methods: GET
token required: no

name: delete_user()
endpoint: /user/delete/
methods: DELETE
token required: yes


ENDPOINTS FOR PETS

name: get_user_pets()
endpoint: /user/<user_id>/pets/
methods: GET
token required: no

name: add_pet()
endpoint: /pet/add/
methods: POST
token required: yes
input JSON params:

name: get_pet()
endpoint: /pet/<pet_id>/
methods: GET
token required: no

name: update_pet()
endpoint: /pet/<pet_id>/update/
methods: PUT
token required: yes
input JSON params:

name: delete_pet()
endpoint: /pet/<pet_id>/delete/
methods: DELETE
token required: yes


ENDPOINTS FOR PETSIT REQUESTS


ENDPOINTS FOR REVIEWS


ENDPOINTS FOR PAYMENTS