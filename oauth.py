from datetime import timedelta
import requests_oauthlib
from flask import Flask, url_for

app = Flask(__name__)
app.secret_key = "111"
app.permanent_session_lifetime = timedelta(days=365)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Init123#@localhost:5432/pizza_shop"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


session = requests_oauthlib.OAuth2Session(
    client_id='Ov23li1dXZso1zRRnSoW',
    redirect_uri='http://127.0.0.1:5000',
    scope=['repo', 'user'],
)

authorization_url, state = session.authorization_url('https://github.com/login/oauth/authorize')
print('Please go here and authorize:', authorization_url)

# Get access token
token_url = 'https://github.com/login/oauth/access_token'
redirect_response = input('Paste the full redirect URL here:')
token = session.fetch_token(token_url, authorization_response=redirect_response, client_secret='9ba4eeb75555f266337f202c9508ce2b76f1fd0d')
print(token)

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['0']
        self.consumer_secret = credentials['111']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class FacebookSignIn(OAuthSignIn):
    pass

class TwitterSignIn(OAuthSignIn):
    pass