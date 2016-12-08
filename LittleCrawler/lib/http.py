#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 2016/8/17 22:37
# file: __init__.py

from __future__ import unicode_literals
from __future__ import print_function
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers
from requests import HTTPError
from pyquery import PyQuery
from LittleCrawler import utils
try: from requests.utils import get_encoding_from_content
except ImportError: get_encoding_from_content = None
import six
import json
import chardet
import lxml.html
import lxml.etree

__all__ = ['HTTP_METHOD','Request','Response','rebuild_response']

HTTP_METHOD = ('GET', 'POST', 'PUT', 'DELETE')


class Request(object):
    """
    The HTTP Request Object 
    and it has the below property
    """

    __slots__ = ('url','method','data',
        'user_agent','headers','cookies',
        'save','timeout',
        'js','load_images','load_css','wait_before_end',
        'js_view_width','js_view_height',
        'js_script','js_run_at',
        'clear_cookies')
    
    def __init(self):
        self.url = None
        self.method = 'GET'   # default to be the 'GET' method
        self.data = None
        self.user_agent = None
        self.headers = {}
        self.cookies = {}
        self.save = None
        self.timeout = 10000
        self.js = False
        self.load_images = False
        self.load_css = False
        self.wait_before_end = 10
        self.js_view_width = 1366
        self.js_view_height = 768
        self.js_script = None        
        self.clear_cookies = False

    def __init__(self,**kwargs):
        self.__init()
        for each in kwargs:
            setattr(self,each,kwargs[each])

    def __str__(self):
        return '\n'.join(('{0}: {1}'.format(each,getattr(self,each,None)) \
            for each in self.__slots__))
    
    def __repr__(self):
        """For pretty visual."""
        return json.dumps(dict(((each,getattr(self,each,None)) for each in self.__slots__)),indent=4)
        


class Response(object):
    """    
    The HTTP Response Object 
    and it has the below property
    """
    __slots__ = ('status_code','ok','error',
        'url','origin_url','headers','cookies',
        'encoding','__encoding','text','__text','content',
        'doc','__doc','etree','__elements','json','__json',
        'time','js_script_result',
        'save','request_data')

    def __init(self):
        self.status_code = 0
        self.error = None
        self.url = None
        self.origin_url = None
        self.headers = {}
        self.cookies = {}
        self.encoding = None
        self.__encoding = None
        self.__text = ''
        self.content = ''
        self.__doc = None
        self.__elements = None
        self.__json = None
        self.time = 0
        self.js_script_result = None
        self.save = None
        self.request_data = None

    def __init__(self,**kwargs):
        self.__init()
        for each in kwargs:
            setattr(self,each,kwargs[each])

    def __str__(self):
        return '\n'.join(('{0}: {1}'.format(each,getattr(self,each,None)) \
            for each in self.__slots__))
    
    def __repr__(self):
        """For pretty visual."""
        return json.dumps(dict(((each,getattr(self,each,None)) for each in self.__slots__)),indent=4)
 
    
    def __bool__(self):
        """Return true if 'stauts_code' is 200 and no errors. """
        return self.ok
    
    def __nonzero__(self):
        """Return true if 'stauts_code' is 200 and no errors. """
        return self.ok

    @property
    def ok(self):
        try:
            self.raise_for_status()
            return True
        except:
            return False

    @property
    def encoding(self):
        """
        encoding of Response.content.

        if Response.encoding is None, encoding will be guessed
        by header or content or chardet if available.
        """
        if hasattr(self,'__encoding'):
            return self.__encoding
        if isinstance(self.content,six.text_type):
            return 'unicode'
        
        encoding = get_encoding_from_headers(self.headers)
        if encoding == 'ISO-8859-1':
            encoding = None
        if not encoding and get_encoding_from_content:
            if six.PY3:
                encoding = get_encoding_from_content(utils.pretty_unicode(self.content[:200]))
            else:
                encoding = get_encoding_from_content(self.content)
            encoding = encoding and encoding[0] or None
        
        if not encoding and chardet:
            encoding = chardet.detect(self.content)['encoding']
        
        if encoding and encoding.lower() == 'gb2312':
            encoding = 'gb18030'
        
        self.__encoding = encoding or 'utf-8'
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        self.__encoding = value
        self.__text = None

    @property
    def text(self):
        """
        Content of the response, in unicode.

        if Response.encoding is None and chardet is available,
        encoding will be guessed
        """
        if hasattr(self, '__text') and self.__text:
            return self.__text
        if not self.content:
            return ''
        if isinstance(self.content,six.text_type):
            return self.content

        # decode unicode from giving encoding
        try:
            self.__text = self.content.decode(self.encoding,'replace')
        except LookupError:
            self.__text = self.content.decode('utf-8','replace')
        return self.__text 
    @property
    def doc(self):
        if hasattr(self, '__doc'): return self.__doc
        self.__doc = PyQuery(self.etree)
        self.__doc.make_links_absolute(self.url)
        return self.__doc

    @property
    def etree(self):
        if not hasattr(self,'__elements') and self.content:
            try:
                parser = lxml.html.HTMLParser(encoding=self.encoding)
                self.__elements = lxml.html.fromstring(self.content,parser=parser)
            except LookupError:
                self.__elements = lxml.html.fromstring(self.content)
        if isinstance(self.__elements, lxml.etree._ElementTree):
            self.__elements = self.__elements.getroot()
        return self.__elements

    @property
    def json(self):
        if hasattr(self, '__json'):
            return self.__json
        try: self.__json = json.loads(self.text or self.content)
        except ValueError: self.__json = None
        return self.__json

    def raise_for_status(self, allow_redirects=True):
        """Raises stored :class:`HTTPError` or :class:`URLError`, if one occurred."""

        if self.status_code == 304:
            return
        elif self.error:
            http_error = HTTPError(self.error)
        elif (self.status_code >= 300) and (self.status_code < 400) and not allow_redirects:
            http_error = HTTPError('%s Redirection' % (self.status_code))
        elif (self.status_code >= 400) and (self.status_code < 500):
            http_error = HTTPError('%s Client Error' % (self.status_code))
        elif (self.status_code >= 500) and (self.status_code < 600):
            http_error = HTTPError('%s Server Error' % (self.status_code))
        else:
            return

        http_error.response = self
        raise http_error

    def isok(self):
        return self.ok


def rebuild_response(r):
    response = Response()
    response.status_code = r.get('status_code', 599)
    response.url = r.get('url', '')
    response.headers = CaseInsensitiveDict(r.get('headers', {}))
    response.content = r.get('content', '')
    response.cookies = r.get('cookies', {})
    response.error = r.get('error')
    response.time = r.get('time', 0)
    response.origin_url = r.get('origin_url', response.url)
    response.js_script_result = r.get('js_script_result')
    response.save = r.get('save')
    return response


if __name__ == '__main__':
    request = Request()
    print(request.__str__())
    print(`request`)
    response = Response(url='http:\\www.baidu.com')
    print(response.__str__())
    print(`response`)