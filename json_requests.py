# -*- coding: utf-8 -*-
"""
Small helper module to reduce some requests boilerplate, especially when
used with json data

TODO: refactor to get rid of code duplication between module level functions
and methods of the class

"""

import json
import requests


def post_json(url, data=None, extra_headers=None, validate=False, **kwargs):
    return _request('post', url, data, extra_headers, validate, **kwargs)
post = post_json


def put_json(url, data=None, extra_headers=None, validate=False, **kwargs):
    return _request('put', url, data, extra_headers, validate, **kwargs)
put = put_json


def delete_json(url, data=None, extra_headers=None, validate=False, **kwargs):
    return _request('delete', url, data, extra_headers, validate, **kwargs)
delete = delete_json


def get_json(url, data=None, extra_headers=None, validate=False, **kwargs):
    return _request('get', url, data, extra_headers, validate, **kwargs)
get = get_json


def _request(method, url, data=None, extra_headers=None,
             validate=False, **kwargs):
    request_params = {
        'method': method,
        'url': url,
    }
    request_headers = {
        'Content-Type': 'application/json'
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


class RequestContext(object):
    def __init__(self, base_url=None, **kwargs):
        self.base_url = base_url
        self.request_params = {
            'headers': {
                'Content-Type': 'application/json',
            }
        }
        self.request_params.update(kwargs)

    def get(self, key):
        return self.request_params.get(key)

    def set(self, key, name):
        self.request_params[key] = name

    def delete(self, key):
        del self.request_params[key]

    def post_json(self, url=None, data=None, extra_headers=None,
                  validate=False, **kwargs):
        return self.request('post', url, data, extra_headers, validate,
                            **kwargs)
    post = post_json

    def put_json(self, url=None, data=None, extra_headers=None,
                 validate=False, **kwargs):
        return self.request('put', url, data, extra_headers, validate,
                            **kwargs)
    put = put_json

    def delete_json(self, url, data=None, extra_headers=None, validate=False,
                    **kwargs):
        return self.request('delete', url, data, extra_headers, validate,
                            **kwargs)
    delete = delete_json

    def get_json(self, url, data=None, extra_headers=None, validate=False,
                 **kwargs):
        return self.request('get', url, data, extra_headers, validate,
                            **kwargs)
    get = get_json

    def _build_url(self, url):
        if self.base_url and url:
            return '/'.join([
                self.base_url.rstrip('/'),
                url.lstrip('/')
            ])
        if not self.base_url and not url:
            raise ValueError('Missing URL')

        return self.base_url or url

    def request(self, method, url, data=None, extra_headers=None,
                validate=False, **kwargs):
        request_params = self.request_params.copy()
        request_params['method'] = method
        request_params['url'] = self._build_url(url)
        if data:
            request_params['data'] = json.dumps(data)
        if extra_headers:
            request_params['headers'].update(extra_headers)

        request_params.update(kwargs)
        _validate = request_params.pop('validate', validate)
        response = requests.request(**request_params)
        if _validate:
            response.raise_for_status()
        return response
