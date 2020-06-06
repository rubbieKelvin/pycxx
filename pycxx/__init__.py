import json
import string
from base64 import *
from datetime import datetime, timedelta

CHARS = string.printable
DTFORMAT = "%Y-%m-%d %H:%M:%S.%f"

class IncorrectKeyError(Exception): pass
class CorruptDataError(Exception):  pass

class Cxx(object):
    def __init__(self, key="cxx", expires:int=0):
        super(Cxx, self).__init__()
        self.exp = expires      # seconds:int
        self.key = key          # string
        
    def _mkrngs(key):
        inner = list(CHARS)
        outer = list(CHARS)
        shift = len(key)%26
        
        chunk = outer[:shift]
        del outer[:shift]
        outer += chunk
        
        return inner, outer
        

    def encrypt(self, **kwargs):
        created = datetime.now()
        if self.exp == 0:
            expires = 0
        else:
            expires = created+timedelta(seconds=self.exp)
        data = bytes(json.dumps(kwargs), "utf8")
        data = b16encode(data)
        data = b85encode(data)
        data = data.decode("utf8")
        key = b32encode(bytes(self.key, "utf8"))
        res = json.dumps(dict(
        	created=str(created),
        	expires=str(expires),
        	data = data
        ))
        
        result = key.decode("utf8")+res
        res = ""
        inner, outer = Cxx._mkrngs(self.key)
        
        for char in result:
            if char not in inner:
                res += char
                continue
            i = inner.index(char)
            res += outer[i]
            _c = outer[0]
            del outer[0]
            outer += [_c]
            
        return res
        
    @staticmethod
    def decrypt(string, key):
        inner, outer = Cxx._mkrngs(key=key)
        deckey = b32encode(bytes(key, "utf8"))
        deckey = deckey.decode("utf8")
        res = ""
        
        for char in string:
            if char not in inner:
                res += char
                continue
            i = outer.index(char)
            res += inner[i]
            _c = outer[0]
            del outer[0]
            outer += [_c]
            
        # check for password
        if res[:len(deckey)]==deckey:
            
            # check if data has expired
            _d = res[len(deckey):]
            data = json.loads(_d)
            if data["expires"] != "0":
                created = datetime.strptime(data["created"], DTFORMAT)
                expires = datetime.strptime(data["expires"], DTFORMAT)
                now = datetime.now()
                delta = now-expires
                if delta.seconds>0 and delta.days>-1:
                    raise CorruptDataError("this encrypted string has expired")
                else:
                
                    # extract data
                    data = bytes(data["data"], "utf8")
                    data = b85decode(data)
                    data = b16decode(data)
                    return json.loads(data.decode("utf8"))
            else:
                data = bytes(data["data"], "utf8")
                data = b85decode(data)
                data = b16decode(data)
                return json.loads(data.decode("utf8"))
       
        else:
            raise IncorrectKeyError('the key "%s" is invalid.' %key)
            
        return None

