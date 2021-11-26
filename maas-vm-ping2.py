#import oauth.oauth as oauth
import httplib2
#import urllib.parse
import uuid

from oauthlib.oauth1.rfc5849 import SIGNATURE_PLAINTEXT
#from authlib.integrations.requests_client import OAuth1Session
#from authlib.integrations.requests_client import OAuth1Auth
#from requests_oauthlib import OAuth1, Oauth1Session
from oauthlib import oauth1
import requests

#consumer key ids the user
#secret is the user "password"
#key must be the token?
def perform_API_request(site, uri, method, key, secret, consumer_key):
    resource_tok_string = "oauth_token_secret=%s&oauth_token=%s" % (
        secret, key)
    resource_token = oauth.OAuthToken.from_string(resource_tok_string)
    consumer_token = oauth.OAuthConsumer(consumer_key, "")

    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer_token, token=resource_token, http_url=site,
        parameters={'oauth_nonce': uuid.uuid4().hex})
    oauth_request.sign_request(
        oauth.OAuthSignatureMethod_PLAINTEXT(), consumer_token,
        resource_token)
    headers = oauth_request.to_header()
    url = "%s%s" % (site, uri)
    http = httplib2.Http()
    return http.request(url, method, body=None, headers=headers)

def perform_API_request2(uri, method, consumer_key, 
    token_key, token_secret):

    client = oauth1.Client(
        consumer_key, 
        resource_owner_key=token_key,
        resource_owner_secret=token_secret,
        signature_method=SIGNATURE_PLAINTEXT
    )
    uri, headers, body = client.sign(uri)
    print (headers)
    print(uri)
    print(body)
    http = httplib2.Http()
    print(http.request(uri, "GET", 
        body=None, headers=headers))
    

# API key = '<consumer_key>:<key>:<secret>'
API_KEY = "my8Qy38xaXmC3YPu6c:3DvdC8V3Q6uPvnC4aw:fRdvtCFeXfc7qsyEwPAPgGF94mNQgfKm"
[consumer_key, token_key, token_secret] = API_KEY.split(':')
response = perform_API_request2(
    'http://192.168.200.16:5240/MAAS/api/2.0/nodes/?op=list', 'GET', consumer_key, token_key,
    token_secret)