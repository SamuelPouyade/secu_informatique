import hashlib
import time


def text_to_md5(text: str) -> str:
    """
    Convertit un texte en hash MD5
    :param text: le message à convertir
    :return: le hash MD5
    """
    return hashlib.md5(text.encode()).hexdigest()


if __name__ == "__main__":
    hash_to_get = "5a74dd4eef347734c8a0a9a3188abd11"
    file_name = "rockyou.txt"
    rockyou = open(file_name, "r", encoding="latin-1")

    timer_start = time.time()

    print(f"Recherche du hash {hash_to_get} dans le fichier {file_name}...")
    for password in rockyou:
        formatted_password = password.strip()
        if text_to_md5(formatted_password) == hash_to_get:
            timer_end = time.time()
            print(f"Le mot de passe est : {formatted_password}")
            print(f"Temps d'exécution : {round(timer_end - timer_start, 2)} secondes")
            exit(0)

    print("Le mot de passe n'a pas été trouvé")