import json
from requests import HTTPError, Response as HTTPResponse
import json_requests
from json_requests import *

from pytest import fixture, mark, raises
from mock import patch, MagicMock


@fixture
def context(url):
    return RequestContext(url)


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
def response404():
    response = HTTPResponse()
    response.status_code = 404
    return response


@fixture
def response200():
    response = HTTPResponse()
    response.status_code = 200
    return response


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
        method=method, url=url, data=json.dumps(data), auth=auth,
        headers=headers)


@patch('json_requests.requests')
def test_request_returns_HTTPResponse(requestlib, url, data, headers):
    mock_response = MagicMock()
    requestlib.request.return_value = mock_response
    response = request('post', url, data)
    assert response == mock_response


@patch('json_requests.requests')
def test_request_raises_on_400(requestlib, response404, url, data, headers):
    requestlib.request.return_value = response404
    with raises(HTTPError):
        request('post', url, data, validate=True)


def test_RequestContext_get_set_del_param(context):
    context.set_param('foo', 'bar')
    assert context.request_params['foo'] == 'bar'
    assert context.get_param('foo') == 'bar'
    context.delete_param('foo')
    assert context.get_param('foo') is None


@mark.parametrize('method,http_method', [
    ('post_json', 'post'),
    ('get_json', 'get'),
    ('put_json', 'put'),
    ('delete_json', 'delete')
])
def test_RequestContext_post_all_calls_request(context, method, http_method,
                                               url):
    with patch.object(json_requests.RequestContext, 'request') as request:
        getattr(context, method)(url)
        request.assert_called_once_with(http_method, url, None, None, False)


@mark.parametrize('method,http_method', [
    ('post', 'post'),
    ('get', 'get'),
    ('put', 'put'),
    ('delete', 'delete')
])
def test_RequestContext_post_all_calls_work_with_aliases(context, method,
                                                         http_method, url):
    with patch.object(json_requests.RequestContext, 'request') as request:
        getattr(context, method)(url)
        request.assert_called_once_with(http_method, url, None, None, False)


def test__build_url(context):
    assert (context._build_url('index.html') ==
            'http://some.url.com/index.html')
    assert (context._build_url('/index.html') ==
            'http://some.url.com/index.html')
    assert context._build_url() == 'http://some.url.com'
    context.base_url = None
    assert context._build_url('index.html') == 'index.html'
    with raises(ValueError):
        context._build_url()


@patch('json_requests.requests')
def test_RequestContext_request1(requestlib, context, headers):
    context.request('post', 'foo/bar')
    requestlib.request.assert_called_with(
        method='post', url='http://some.url.com/foo/bar', headers=headers)


@patch('json_requests.requests')
def test_RequestContext_request2(requestlib, context, headers):
    context.request('post', 'foo/bar')
    requestlib.request.assert_called_with(
        method='post', url='http://some.url.com/foo/bar', headers=headers)
    context.request('put', 'foo', {'bar': 'baz'}, extra_headers={
        'User-Agent': 'py.test'})

    requestlib.request.assert_called_with(
        method='put', url='http://some.url.com/foo', headers={
            'Content-Type': 'application/json',
            'User-Agent': 'py.test'
        }, data='{"bar":"baz"}')


@patch('json_requests.requests')
def test_RequestContext_request_raises_on_400(requestlib, response404, context,
                                              headers):
    requestlib.request.return_value = response404
    with raises(HTTPError):
        context.request('post', 'customer/1', validate=True)


@patch('json_requests.requests')
def test_RequestContext_request_doesnt_raise_on_200(requestlib, response200,
                                                    context, headers):
    requestlib.request.return_value = response200
    context.request('put', 'customer/1', validate=True)
