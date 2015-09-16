import requests
from rest_framework import status
from behave import when, given, then


@when(u'I query the Users API')
def step_impl(context):
    # Set up request parameters.
    endpoint = context.server_url + '/api/users'
    headers = {
        'Accept': 'application/json; indent=4',
    }
    params = None
    
    context.response = requests.get(endpoint, headers=headers, params=params, auth=(context.username, context.password))


@then(u'I get a list of Users')
def step_impl(context):

    response = context.response
    response_content = response.json()

    usernames = [result['username'] for result in response_content['results']]

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertIn(context.username, usernames)
    

@then(u'I will be presented with an authentication error')
def step_impl(context):

    response = context.response
    response_content = response.json()

    authentication_errors = ['You do not have permission to perform this action.',
                             'Invalid username/password.',]

    context.test.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    context.test.assertIn(response_content['detail'], authentication_errors)
