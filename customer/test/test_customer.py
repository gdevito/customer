import json
import pytest
from random import *
import requests
from time import time
import tornado
from customer import server

@pytest.fixture
def app():
    return server.customer_app()

@pytest.mark.gen_test
def test_list_customers(http_client, base_url):
    # below uuid is determined alread in customers table
    test_uid = '8eca6474-dfaa-4885-81f1-56bc2ae645c7'
    start_time = time()
    response = yield http_client.fetch(base_url+'/customer?uuid='+test_uid)
    # each pytest-tornado fetch creates a separate test server instance of
    # app on some port via base_url. Requests yielding within .1 seconds are
    # safely under the .1 second response time
    total_time = time() - start_time
    assert total_time < .1
    print response
    assert response.code == 200

@pytest.mark.gen_test
def test_create_customer(http_client, base_url):

    test_num = str(randint(1, 1000))
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    data = {'username' : 'TestUser'+test_num,
            'address' : 'Test Address '+test_num,
            'income' : test_num}
    start_time = time()
    response = yield http_client.fetch(base_url+'/customer',
                                       method='PUT',
                                       body=json.dumps(data))
    total_time = start_time - time()
    assert total_time < 0.1
    print response
    assert response.code == 200

@pytest.mark.gen_test
def test_create_customer_negative(http_client, base_url):

    test_num = str(randint(1, 1000))
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}
    data = {'user' : 'TestUser'+test_num,
            'addr' : 'Test Address '+test_num,
            'income' : test_num}
    try:
        response = yield http_client.fetch(base_url+'/customer',
                                           method='PUT',
                                           body=json.dumps(data))
        print response
    except tornado.httpclient.HTTPError as e:
        assert e.response.code == 500
