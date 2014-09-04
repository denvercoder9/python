# -*- coding: utf-8 -*-
"""
Small helper module to reduce some requests boilerplate, especially when
used with json data
"""

import json
import requests


def post_json(url, data=None, extra_headers=None, validate=True, **kwargs):
    return request('post', url, data, extra_headers, validate, **kwargs)


def put_json(url, data=None, extra_headers=None, validate=True, **kwargs):
    return request('put', url, data, extra_headers, validate, **kwargs)


def delete_json(url, data=None, extra_headers=None, validate=True, **kwargs):
    return request('delete', url, data, extra_headers, validate, **kwargs)


def get_json(url, data=None, extra_headers=None, validate=True, **kwargs):
    return request('get', url, data, extra_headers, validate, **kwargs)


def request(method, url, data=None, extra_headers=None,
            validate=True, **kwargs):
    request_params = {
        'method': method,
        'url': url,
    }
    request_headers = {
        'content-type': 'application/json'
    }
    if data:
        request_params['data'] = json.dumps(data)
    if extra_headers:
        request_headers.update(extra_headers)
    request_params['headers'] = request_headers
    request_params.update(kwargs)

    response = requests.request(**request_params)
    if validate:
        response.raise_for_status()
    return response
