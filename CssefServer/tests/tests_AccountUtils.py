import unittest
import cssefserver

class PasswordHashTest(unittest.TestCase):
    """Tests cssefserver.account.utils.PasswordHash
    """
    def test_new_utf8_hash(self):
        plaintext_secret = "7hi$ isa p!aint3xt passw0rd"
        rounds = 5
        hash_obj = cssefserver.account.utils.PasswordHash.new(plaintext_secret, rounds)
        self.assertTrue(isinstance(hash_obj, cssefserver.account.utils.PasswordHash))

    def test_new_hash_from_unicode(self):
        plaintext_secret = u"UNICODE password h3re"
        rounds = 5
        hash_obj = cssefserver.account.utils.PasswordHash.new(plaintext_secret, rounds)
        self.assertTrue(isinstance(hash_obj, cssefserver.account.utils.PasswordHash))

    def test_from_existing_hash_string(self):
        phrase_text = "7hi$ isa p!aint3xt passw0rd"
        phrase_hash = "$2b$05$gubbsSVmiLWdBN28fjl0p.69iDxyuUjpCX/9B6ypIDRUTKvxDv.2q"
        hash_obj = cssefserver.account.utils.PasswordHash(phrase_hash)
        self.assertTrue(isinstance(hash_obj, cssefserver.account.utils.PasswordHash))
        self.assertTrue(str(hash_obj), phrase_hash)

    def test_equals(self):
        phrase_text = "7hi$ isa p!aint3xt passw0rd"
        phrase_hash = "$2b$05$gubbsSVmiLWdBN28fjl0p.69iDxyuUjpCX/9B6ypIDRUTKvxDv.2q"
        hash_obj = cssefserver.account.utils.PasswordHash(phrase_hash)
        self.assertTrue(hash_obj == phrase_text)
        self.assertFalse(hash_obj == None)
        self.assertFalse(hash_obj == "this is not equal to the phrase")
        self.assertFalse(hash_obj == u"this is an incorrect unicode string")

class AuthorizeAccessTest(unittest.TestCase):
