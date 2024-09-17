import hashlib
import time


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

    timer_start = time.time()

    for password in rockyou:
        if text_to_hash(password.strip()) == hash_to_get:
            timer_end = time.time()
            print(f"Le mot de passe est : {password}")
            print(f"Temps d'exécution : {round(timer_end - timer_start, 2)} secondes")
            break

