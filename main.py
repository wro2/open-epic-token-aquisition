#-------------------------------------------
# Class Name: fhir_authorization
# Description: This class is responsible for aquiring an access token from an EPIC FHIR Authorization server
#              Any token received is assumed to be valid. This code stub is not checking token signature with OpenID
#              This code will print the aquired access token to the console \ terminal window.
#             
#               Note: This is a raw HTTP request for demonstration and does not use any 3rd party FHIR Libraries.
#
# 3rd Party Library Dependencies: 
#
# Requests Library - Used for Making HTTP Request - https://docs.python-requests.org/en/latest/
# PyJWT - Used to create Java Web Tokens https://pypi.org/project/jwt/
#-------------------------------------------

import json
import requests 
import jwt 
import string
import random
import ssl

from datetime import datetime, timedelta, timezone
from requests.structures import CaseInsensitiveDict
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime
#----------------------------------------
#START CONFIGURATION SECTION -- MAKE CHANGE HERE FOR CLIENT ID & URL
#----------------------------------------    

#Enter your Epic Client ID Below:
client_id = '<ENTER CLIENT ID HERE>'

#Epic Public Sandbox OAuth URL Below:
token_uri = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"  

#----------------------------------------
#END CONFIGURATION SECTION -- MAKE CHANGE HERE FOR CLIENT ID & URL
#----------------------------------------   


#----------------------------------------
# START BUILD JWT
# https://fhir.epic.com/Documentation?docId=oauth2&section=BackendOAuth2Guide
#----------------------------------------    
#Generate random string for GTI (cannot exceed 150 chars)    
jti_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 150)) 

instance = JWT()
message = {    
    'iss': client_id,
    'sub': client_id,
    'aud': token_uri,        
    'jti': jti_string,    
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),
    'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(minutes=4)),
}

# Load the private RSA signing key from a PEM file named privatekey.pem and sign the JWT)
with open('./keys/privatekey.pem', 'rb') as fh:
    signing_key = jwk_from_pem(fh.read())

#Generate the JWS
compact_jws = instance.encode(message, signing_key, alg='RS384')
#----------------------------------------
#END Build JWT
#----------------------------------------

#----------------------------------------
# START Create HTTPS Post requesting token
#----------------------------------------    
headers = CaseInsensitiveDict()
headers['Content-Type'] = 'application/x-www-form-urlencoded'

data = {
'grant_type': 'client_credentials',
'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
'client_assertion': compact_jws }

print("\n ----START DEBUG INFORMATION -----  \n")
print("\nJWT Token: \n"  + compact_jws + "\n")
print("----END DEBUG INFORMATION -----  \n")

#Perform HTTP Request (Caution: Disabled SSL Certification Validation for Testing Purposes) 
requestResponse = requests.post(token_uri, headers=headers, data=data, verify=False) 
response_json_format = json.loads(requestResponse.text)
access_token = response_json_format.get('access_token')

#Debug Code
print("\n ----ACCESS TOKEN INFO ----- ")
if(access_token is None):
    print( "\n""Request ERROR| No Access Token because: " + response_json_format.get('error'))      
else:
    print( "\n" + "OAUTH ACCESS TOKEN AQUIRED (BELOW): \n--------- \n" + access_token + "\n-----------")
    print("\n" + "Execute Post - END", (datetime.now()).strftime("%d/%m/%Y %H:%M:%S"))


#----------------------------------------
# END Create HTTPS Post requesting token
#---------------------------------------- 
