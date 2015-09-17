import hashlib
import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from behave import when, given, then

User = get_user_model()

@when(u'I query the "{text}" API')
def step_impl(context, text):
    # Set up request parameters.
    endpoint = context.server_url + '/api/%s' % text.lower()
    headers = {
        'Accept': 'application/json; indent=4',
    }
    params = None
    
    auth = (context.username, context.password) if context.username else None
    context.response = requests.get(endpoint, headers=headers, params=params, auth=auth)


@then(u'I will be presented with an authentication error')
def step_impl(context):

    response = context.response
    response_content = response.json()

    authentication_errors = ['You do not have permission to perform this action.',
                             'Invalid username/password.',]

    context.test.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    context.test.assertIn(response_content['detail'], authentication_errors)


@then(u'I get a list of all Users')
def step_impl(context):

    response = context.response
    response_content = response.json()
    results = response_content['results']
    count = response_content['count']

    usernames = [result['username'] for result in response_content['results']]
    user_count = len(User.objects.all())

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertEqual(count, user_count)
    context.test.assertIn(context.username, usernames)


@then(u'I get a list containing my User')
def step_impl(context):

    response = context.response
    response_content = response.json()
    results = response_content['results']
    count = response_content['count']

    usernames = [result['username'] for result in results]

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertEqual(count, 1)
    context.test.assertIn(context.username, usernames)


@then(u'I get an empty list')
def step_impl(context):

    response = context.response
    response_content = response.json()
    results = response_content['results']
    count = response_content['count']

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertEqual(count, 0)


@then(u'I get a Registration Token')
def step_impl(context):

    response = context.response
    response_content = response.json()

    token_hash = hashlib.sha256('1234'.encode()).hexdigest()

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertEqual(response_content['token'], token_hash)
