import config


def substitute(message: bytes, alp: bytes, key: bytes, skip: bytes = None) -> list:
    """
    Шифр простой замены

    :param message: сообщение для зашифрования
    :param alp: алфавит
    :param key: ключ для замены
    :param skip: специальные символы, которые требуется пропускать при замене
    :return: зашифрованное сообщение
    """
    result = []
    for letter in message:

        idx = -1
        for i in range(len(alp)):
            if letter == alp[i] and letter not in skip:
                idx = i
                break
        if idx != -1:
            result.append(key[idx])
        else:
            result.append(letter)
    return result


class Encryptor:

    def __init__(self, name, params: dict):
        self.name = name
        self.params = params
        pass

    def encrypt(self, message: bytes) -> bytes:
        pass

    def decrypt(self, message: bytes) -> bytes:
        pass

    def __repr__(self):
        return f"Encryptor({self.name})"


class SubstitutionEncryptor(Encryptor):

    def __init__(self, params: dict):
        super(SubstitutionEncryptor, self).__init__("substitution", params)
        self.alphabet = self.params.get("alphabet")
        self.key = self.params.get("key")

    def encrypt(self, message: bytes) -> bytes:
        return bytes(substitute(message, self.alphabet, self.key))

    def decrypt(self, message: bytes) -> bytes:
        return bytes(substitute(message, self.key, self.alphabet))


def get_encryptor() -> Encryptor:
    # TODO: может стоит вспомнить про букву O из слова SOLID
    return SubstitutionEncryptor(config.ENCRYPTION_MODE.get("params"))

    # python 3.10 will wait...
    # match config.ENCRYPTION_MODE:
    #     case {"name": "substitution", "params": params}:
    #         return SubstitutionEncryptor(params)
    #     case {"name": name, "params": _}:
    #         raise ValueError(f"Режим шифрования {name} не поддерживается")
    #     case _:
    #         raise ValueError(f"Режим шифрования не выбран")


def encrypt_flags(message: bytes, encryptor: Encryptor) -> bytes:
    """
    Шифрует все флаги в переданном аргументе message и возвращает
    полученную строку

    :param message:     сообщение с флагами
    :param encryptor:   экземпляр класса Encryptor, реализующий
                        какой-либо алгоритм шифрования
    :return:            зашифрованное сообщение
    """
    return config.FLAG_FORMAT.sub(lambda x: encryptor.encrypt(x.group()), message)


def decrypt_flags(message: bytes, encryptor: Encryptor) -> bytes:
    """
    Расшифровывает все флаги в переданном аргументе message и возвращает
    полученную строку

    :param message:     сообщение с зашифрованными флагами
    :param encryptor:   экземпляр класса Encryptor, реализующий
                        какой-либо алгоритм шифрования
    :return:            расшифрованное сообщение
    """
    return config.ENCRYPTED_FLAG_FORMAT.sub(lambda x: encryptor.decrypt(x.group()), message)
