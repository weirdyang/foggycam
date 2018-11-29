# Tests for the FoggyCam core class.

import sys
sys.path.append('../')

import os.path
import pytest
import json
import pickle
from http.cookiejar import CookieJar, Cookie
from foggycam import FoggyCam

def test_foggycam_unpickle_cookies():
    foggycam = FoggyCam("joey-tribianni","how-you-doin")
    
    cztoken_cookie = Cookie(None, 'cztoken', 'b.000000000', None, None, 'home.nest.com', 
       None, None, '/', None, False, False, 'TestCookie', None, None, None)

    foggycam.cookie_jar.set_cookie(cztoken_cookie)

    foggycam.unpickle_cookies()

    assert foggycam.nest_access_token

def test_pickle_cookies():
    foggycam = FoggyCam("joey-tribianni","how-you-doin")
    foggycam.cookie_jar = CookieJar()

    foggycam.pickle_cookies()
    assert os.path.isfile("cookies.bin") 

def test_initialize_twof_session():
    foggycam = FoggyCam("joey-tribianni","how-you-doin")

    session_json = {"2fa_state": "enrolled", "access_token": "TEST_TOKEN", "primary_phone": "+15555555555", "email": "dummy@localhost", "expires_in": "Sat, 29-Dec-2018 05:14:14 GMT", "urls": {"rubyapi_url": "https://localhost/", "czfe_url": "https://localhost", "log_upload_url": "https://localhost/upload/user", "transport_url": "https://localhost", "weather_url": "https://localhost/weather/v1?query=", "support_url": "https://localhost/support/webapp?", "direct_transport_url": "https://localhost:443"}, "2fa_enabled": True, "userid": "0000000", "2fa_state_changed": "2010-01-01 07:21:55.0", "is_superuser": False, "language": "en_US", "weave": {"service_config": "TEST_SERVICE_TOKEN", "pairing_token": "TEST_PAIRING_TOKEN", "access_token": "TEST_ACCESS_TOKEN"}, "limits": {"thermostats_per_structure": 0, "structures": 0, "smoke_detectors_per_structure": 0, "smoke_detectors": 0, "thermostats": 0}, "user": "user.0000000", "is_staff": False}

    foggycam.nest_access_token = session_json['access_token']
    foggycam.nest_access_token_expiration = session_json['expires_in']
    foggycam.nest_user_id = session_json['userid']

    assert foggycam.nest_access_token
    assert foggycam.nest_access_token_expiration
    assert foggycam.nest_user_id

    foggycam.pickle_cookies()
    assert os.path.isfile("cookies.bin")
