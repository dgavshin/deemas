import string
from random import shuffle, randint, choices
from string import ascii_letters
from unittest import TestCase, main
from unittest.mock import MagicMock, call

from server import Encryptor, encrypt_flags, decrypt_flags, get_encryptor, config


def init_encryptor() -> Encryptor:
    alp = ascii_letters.encode()
    key = [x for x in ascii_letters]
    shuffle(key)
    key = "".join(key).encode()
    config.ENCRYPTION_MODE.get("params")["key"] = key
    config.ENCRYPTION_MODE.get("params")["alphabet"] = alp
    return get_encryptor()


def genflag():
    return (''.join(choices(string.ascii_uppercase + string.digits, k=31)).upper() + "=").encode()


class TestFlagEncryption(TestCase):

    def test_encrypt_no_flags(self):
        encryptor = init_encryptor()
        encryptor.encrypt = MagicMock(return_value=b"encrypted")
        message = b"this is a flags"
        self.assertEqual(encrypt_flags(message, encryptor), b"this is a flags")
        encryptor.encrypt.assert_not_called()

    def test_encrypt_one_flag(self):
        encryptor = init_encryptor()
        encryptor.encrypt = MagicMock(return_value=b"encrypted")
        flag = genflag()
        message = b"this is a flag: " + flag
        self.assertEqual(encrypt_flags(message, encryptor), b"this is a flag: encrypted")

        encryptor.encrypt.assert_called_with(flag)
        
    def test_encrypt_multiple_flags(self):
        encryptor = init_encryptor()
        encryptor.encrypt = MagicMock(return_value=b"encrypted")
        flags = [genflag() for _ in range(3)]
        message = b"this is a flags: " + b" ".join(flags)
        self.assertEqual(encrypt_flags(message, encryptor), b"this is a flags: encrypted encrypted encrypted")
        encryptor.encrypt.assert_has_calls(
            [call(flags[0]), call(flags[1]), call(flags[2])],
            any_order=True)

    def test_decrypt_no_flags(self):
        encryptor = init_encryptor()
        encryptor.decrypt = MagicMock(return_value=b"decrypted")
        message = b"this is a flags"
        self.assertEqual(decrypt_flags(message, encryptor), b"this is a flags")

        encryptor.decrypt.assert_not_called()

    def test_decrypt_one_flag(self):
        encryptor = init_encryptor()
        encryptor.decrypt = MagicMock(return_value=b"decrypted")
        flag = genflag()
        message = b"this is a flag: " + flag
        self.assertEqual(decrypt_flags(message, encryptor), b"this is a flag: decrypted")

        encryptor.decrypt.assert_called_with(flag)

    def test_decrypt_multiple_flags(self):
        encryptor = init_encryptor()
        encryptor.decrypt = MagicMock(return_value=b"decrypted")
        flags = [genflag() for _ in range(3)]
        message = b"this is a flags: " + b" ".join(flags)

        self.assertEqual(decrypt_flags(message, encryptor), b"this is a flags: decrypted decrypted decrypted")
        encryptor.decrypt.assert_has_calls(
            [call(flags[0]), call(flags[1]), call(flags[2])],
            any_order=True)


class TestSubstitutionEncryptor(TestCase):

    def test_valid_str(self):
        encryptor = init_encryptor()

        for i in range(100):
            message_len = randint(1, 20)
            message = ''.join(choices(string.ascii_uppercase + string.digits, k=message_len)).encode()
            ciphertext = encryptor.encrypt(message)
            decrypted = encryptor.decrypt(ciphertext)
            self.assertEqual(message, decrypted)


if __name__ == '__main__':
    main()
