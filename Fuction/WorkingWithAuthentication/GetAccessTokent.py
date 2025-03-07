import requests

# Replace these with your actual values
google_client_id = '610714538108-8854n4spm88u53sd0aadp6a64bns2m5u.apps.googleusercontent.com'
google_client_secret = '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'
authorization_code = 'XoPGqRsIotwz0PWbzTZQG5LKDYSTAfLzIn-j0URmJbBqAzFuTWDsPw=='
redirect_uri = 'https://httptriggerwithauthen.azurewebsites.net/api/HttpTriggerWithAuthen'


#https://httptriggerwithauthen.azurewebsites.net/api/HttpTriggerWithAuthen?code=XoPGqRsIotwz0PWbzTZQG5LKDYSTAfLzIn-j0URmJbBqAzFuTWDsPw==
# URL to exchange authorization code for access token
token_url = 'https://oauth2.googleapis.com/token'

# Data to be sent in the POST request
token_data = {
    'code': authorization_code,
    'client_id': google_client_id,
    'client_secret': google_client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}

# Send POST request to get access token
response = requests.post(token_url, data=token_data)

# Parse the JSON response
token_response = response.json()

# Check if the request was successful
if response.status_code == 200:
    access_token = token_response.get('access_token')
    print(f"Access Token: {access_token}")
else:
    print(f"Error: {token_response.get('error')}")
    print(f"Description: {token_response.get('error_description')}")
