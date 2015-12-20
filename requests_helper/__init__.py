import requests


class Session(requests.Session):
    """
    Small hack to add a base_url attribute to the Session, saves some typing!

    Compare:

    s = Session()
    s.get('http://very-long-and-hairy-url.com/index.html')
    s.get('http://very-long-and-hairy-url.com/profile?id=1')
    s.get('http://very-long-and-hairy-url.com/news.html')

    ... to ...

    s = Session(base_url='http://www.very-long-and-hairy-url.com')
    s.get('/index.html')
    s.get('/profile?id=1')
    s.get('/news.html')
    """

    def __init__(self, **kwargs):
        self.base_url = kwargs.pop('base_url', None)
        super(Session, self).__init__(**kwargs)

    def request(self, method, url, **kwargs):
        if self.base_url:
            url = self.base_url + url
        return super(Session, self).request(method, url, **kwargs)
