import os
import time
from zipfile import ZipFile

from simple_term_menu import TerminalMenu


def list_zip(directory=".") -> list:
    """
    Liste les fichiers .zip dans un répertoire
    :param directory: le répertoire ciblé
    :return: La liste des fichiers .zip
    """
    return list(file for file in os.listdir(directory) if
                os.path.isfile(os.path.join(directory, file)) and file.endswith('.zip'))


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
            yield from get_passwords(size - 1, pwd + char)
    else:
        for char in get_alphabet():
            yield pwd + char


def archive_brute_force(filename: str) -> str:
    """
    Fonction pour brute force une archive zip protégée par mot de passe
    :param filename: le nom de l'archive
    :return: le mot de passe de l'archive
    """
    with ZipFile(filename) as fs:
        # On essaye d'abord sans mot de passe
        try:
            fs.extractall(pwd=bytes('', 'utf-8'))
        except RuntimeError as pwdRequired:
            # On limite la taille du mot de passe à 6 caractères
            for i in range(6):
                pwd_size = i + 1
                print(f"Taille de mot de passe en cours d'essaie : {pwd_size}")
                for password in get_passwords(pwd_size):
                    try:
                        fs.extractall(pwd=bytes(password, 'utf-8'))
                    # La fonction extractall() lève une exception si le mot de passe est incorrect
                    except Exception as wrongPwd:
                        continue
                    return password
            return ""


if __name__ == "__main__":
    # Setup menus de terminal
    main_title = "ZIP Brute force\nChoisissez le fichier à brute forcer..."
    main_options = list_zip()
    main_options.append(None)
    main_options.append("Quitter")
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)

    while True:
        main_entry_index = main_menu.show()
        # Quitter
        if main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)
        # Fichier ZIP choisi
        else:
            timer_start = time.time()
            archive_password = archive_brute_force(main_options[main_entry_index])
            timer_end = time.time()
            if not archive_password:
                print("Aucun mot de passe trouvé")
            else:
                print("Mot de passe trouvé :", archive_password)
            print("Temps d'exécution :", round(timer_end - timer_start, 2), "secondes")
            input("Appuyez sur Entrée pour continuer...")
