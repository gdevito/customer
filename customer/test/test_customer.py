import json
import pytest
from random import *
import requests
from customer import server

@pytest.fixture
def app():
    return server.customer_app()

@pytest.mark.gen_test
def test_list_customers(http_client, base_url):
    test_uid = '8eca6474-dfaa-4885-81f1-56bc2ae645c7'
    response = yield http_client.fetch(base_url+'/customer?uuid='+test_uid)
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
    response = yield http_client.fetch(base_url+'/customer',
                                       method='PUT',
                                       body=json.dumps(data))
    print response
    assert response.code == 200
