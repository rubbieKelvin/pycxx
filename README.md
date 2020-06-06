# Cxx
### simple crypting library

## installation
```bash
pip install cxx
```

## usage
```python
import cxx

c = cxx.Cxx(key="password", expires=0)
"""${expires} is the Time in milliseconds for the 
encrypted password to be destroyed
setting ${encrypted} to 0 implies the data would
not be destroyed
"""

# to encrypt;
data = dict(
    name="rubbie kelvin",
    country="Nigeria"
)
encrypted = c.encrypt(**data) # =>str


# to decrypt
data2 = cxx.Cxx.decrypt(encrypted, key="password") # => dict
```

`made with ❤️ by rubbie`