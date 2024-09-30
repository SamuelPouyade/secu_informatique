from zipfile import ZipFile


def get_alphabet() -> list:
    """
    Fonction pour récupérer les lettres de l'alphabet latin en minuscules
    :return: la liste des lettres minuscules
    """
    alphabet = []
    for i in range(26):
        alphabet.append(chr(ord('a') + i))
    return alphabet


def get_passwords(size, pwd="") -> str:
    """
    Fonction récursive pour générer les mots de passe de taille "size"
    :param size: la taille des mots de passe
    :param pwd: le mot de passe en cours de construction
    :return: les mots de passe
    """
    if size != 1:
        for char in get_alphabet():
            yield from get_passwords(size-1, pwd+char)
    else:
        for char in get_alphabet():
            yield pwd+char


def archive_brute_force(filename: str) -> str:
    """
    Fonction pour brute force une archive zip protégée par mot de passe
    :param filename: le nom de l'archive
    :return: le mot de passe de l'archive
    """
    with ZipFile(filename) as fs:
        try:
            fs.extractall(pwd = bytes('', 'utf-8'))
        except RuntimeError as pwdRequired:
            for i in range(6):
                pwd_size = i + 1
                print(f"Mot de passe essayé : {pwd_size}")
                for password in get_passwords(pwd_size):
                    try:
                        fs.extractall(pwd = bytes(password, 'utf-8'))
                    except Exception as wrongPwd:
                        continue
                    return password
            return ""


if __name__ == "__main__":
    password = archive_brute_force('archive.zip')
    if not password:
        print("Aucun mot de passe trouvé")
    else:
        print("Mot de passe trouvé :", password)
