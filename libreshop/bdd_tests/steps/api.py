import json
import hashlib
import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from behave import when, given, then

User = get_user_model()

@when(u'I query the "{text}" API')
def step_impl(context, text):
    # Set up request parameters.
    endpoint = context.server_url + '/api/%s/' % text.lower()
    headers = {
        'Accept': 'application/json; indent=4',
    }
    params = None
    
    auth = (context.username, context.password) if context.username else None
    context.response = requests.get(endpoint, headers=headers, params=params, auth=auth)


@when(u'I create a new "{model}"')
def step_impl(context, model):
    # Set up request parameters.
    endpoint = context.server_url + '/api/%ss/' % model.lower()
    headers = {
        'Accept': 'application/json; indent=4',
        'Content-type': 'application/json',
    }
    params = None

    data = None
    if model == 'User':
        data = {'username': 'new_user',
                'password': 'new_user',}
        token = getattr(context, 'token', None)
        if token:
            data['token'] = token

        captcha = getattr(context, 'captcha', None)
        if captcha:
            data['captcha'] = captcha

    data = json.dumps(data)
    auth = (context.username, context.password) if context.username else None
    context.response = requests.post(endpoint, headers=headers, params=params, data=data, auth=auth)


@when(u'I update the "{field}" field on a "{model}" object to "{value}"')
def step_impl(context, field, model, value):
    # Set up request parameters.
    endpoint = context.server_url + '/api/%ss/' % model.lower()
    headers = {
        'Accept': 'application/json; indent=4',
        'Content-type': 'application/json',
    }
    params = None

    data = None
    if model == 'User':
        data = {'username': 'user',
                'password': 'user',}
        token = getattr(context, 'token', None)
        if token:
            data['token'] = token

        captcha = getattr(context, 'captcha', None)
        if captcha:
            data['captcha'] = captcha

    data[field] = value

    data = json.dumps(data)
    auth = (context.username, context.password) if context.username else None

    response = requests.get(endpoint, headers=headers, params=params, auth=auth)
    response = response.json()
    urls = [result['url'] for result in response['results']]

    response = None
    for endpoint in urls:
        response = requests.put(endpoint, headers=headers, params=params, data=data, auth=auth)

    if not response:
        response = requests.put(endpoint + '1/', headers=headers, params=params, data=data, auth=auth)

    context.response = response


@when(u'I fail the CAPTCHA')
def step_impl(context):
    context.captcha = '4321'


@when(u'I solve the CAPTCHA')
def step_impl(context):
    context.captcha = '1234'


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


@then(u'I will receive a "{http_status}" response')
def step_impl(context, http_status):

    response = context.response
    status_name = 'HTTP_%s' % http_status.upper().replace(' ', '_')
    status_code = getattr(status, status_name, None)

    context.test.assertEqual(response.status_code, status_code)


@then(u'The response will contain my username')
def step_impl(context):

    response = context.response
    response_content = response.json()
    username = response_content.get('username', None)

    context.test.assertEqual(username, 'new_user')


@then(u'The response will contain an error description')
def step_impl(context):

    response = context.response
    response_content = response.json()
    description = response_content.get('description', None)

    assert description


@then(u'The "{field}" field will equal "{value}"')
def step_impl(context, field, value):

    response = context.response
    response_content = response.json()
    field = response_content.get(field, None)

    context.test.assertEqual(field, value)


@step(u'I get a Registration Token')
def step_impl(context):

    response = context.response
    response_content = response.json()
    token = response_content['token']

    token_hash = hashlib.sha256('1234'.encode()).hexdigest()
    context.token = token

    context.test.assertEqual(response.status_code, status.HTTP_200_OK)
    context.test.assertEqual(token, token_hash)
