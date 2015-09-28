import base64
from social.backends.reddit import RedditOAuth2


# Monkey patch social.backends.reddit.RedditOAuth2 per Issue #688
# at https://github.com/omab/python-social-auth/issues/688
def auth_headers(self):
    return {
        'Authorization': b'Basic ' + base64.urlsafe_b64encode(
            ('{0}:{1}'.format(*self.get_key_and_secret()).encode())
        )
    }

RedditOAuth2.auth_headers = auth_headers
