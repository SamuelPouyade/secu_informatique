import hashlib


def text_to_hash(text: str) -> str:
    """
    Convertit un texte en hash
    :param text: str
    :return: str
    """
    return hashlib.md5(text.encode()).hexdigest()


if __name__ == "__main__":
    hash_to_get = "5a74dd4eef347734c8a0a9a3188abd11"
    rockyou = open("rockyou.txt", "r", encoding="latin-1")

    for password in rockyou:
        print(password.strip())
        if text_to_hash(password.strip()) == hash_to_get:
            print(f"Le mot de passe est : {password}")
            break

