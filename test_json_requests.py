import json
from requests import HTTPError, Response as HTTPResponse
from json_requests import *

from pytest import fixture, mark, raises
from mock import patch, MagicMock


@fixture
def url():
    return 'http://some.url.com'


@fixture
def data():
    return {
        'key': 'value',
        'foo': 'bar',
    }


@fixture
def headers():
    return {
        'Content-Type': 'application/json'
    }


@mark.parametrize('function,method', [
    (post_json, 'post'),
    (get_json, 'get'),
    (put_json, 'put'),
    (delete_json, 'delete')
])
@patch('json_requests.request')
def test_post_all_calls_request(request, function, method, url):
    function(url)
    request.assert_called_once_with(method, url, None, None, False)


@mark.parametrize('function,method', [
    (post, 'post'),
    (get, 'get'),
    (put, 'put'),
    (delete, 'delete')
])
@patch('json_requests.request')
def test_post_all_calls_work_with_aliases(request, function, method, url):
    function(url)
    request.assert_called_once_with(method, url, None, None, False)


@patch('json_requests.requests')
def test_request_with_data(requestlib, url, data, headers):
    method = 'post'
    request(method, url, data)
    requestlib.request.assert_called_with(
        method=method, url=url, data=json.dumps(data), headers=headers)


@patch('json_requests.requests')
def test_request_with_data_and_extra_headers(requestlib, url, data, headers):
    method = 'post'
    request(method, url, data, extra_headers={'foo': 'bar'})
    headers.update(foo='bar')
    requestlib.request.assert_called_with(
        method=method, url=url, data=json.dumps(data), headers=headers)


@patch('json_requests.requests')
def test_request_with_additional_information(requestlib, url, data, headers):
    method = 'post'
    auth = ('user', 'pass')
    request(method, url, data, auth=auth)
    requestlib.request.assert_called_with(
        method=method, url=url, data=json.dumps(data), auth=auth, headers=headers)


@patch('json_requests.requests')
def test_request_returns_HTTPResponse(requestlib, url, data, headers):
    mock_response = MagicMock()
    requestlib.request.return_value = mock_response
    method = 'post'
    response = request(method, url, data)
    assert response == mock_response


@patch('json_requests.requests')
def test_request_raises_on_400(requestlib, url, data, headers):
    response = HTTPResponse()
    requestlib.request.return_value = response
    response.status_code = 400
    method = 'post'
    with raises(HTTPError):
        request(method, url, data, validate=True)
