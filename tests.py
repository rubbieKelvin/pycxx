#!usr/bin/env python
import unittest
import cxx

class EncryptionTest(unittest.TestCase):
    def test_encryption():
        key, data, c = "test", dict(
            name="rubbie"
        ), cxx.Cxx(key=key)
        encrypted = c.encrypt(**data)
        data2 = cxx.Cxx.decrypt(encrypted, key)
        
        print("initial data:", data)
        print("encrypted:", encrypted)
        
        self.assertEqual(
            data, data2, 
            """encrypted data should be the same 
            as the initial data after being decrypted
            """
        )
        
if __name__ == "__main__":
    unittest.main()