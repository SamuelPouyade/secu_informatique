import hashlib
import os
import time

from simple_term_menu import TerminalMenu


def list_hash(file="hashlist", encoding="utf-8"):
    if not os.path.isfile(file):
        open(file, "w+", encoding=encoding).close()
    return (hash_text.strip() for hash_text in open(file, "r", encoding=encoding))


def list_text_files(directory="."):
    return (file for file in os.listdir(directory) if
            os.path.isfile(os.path.join(directory, file)) and file.endswith('.txt'))


def text_to_md5(text: str) -> str:
    """
    Convertit un texte en hash MD5
    :param text: le message à convertir
    :return: le hash MD5
    """
    return hashlib.md5(text.encode()).hexdigest()


def compare_md5_hash_to_file(hash_to_compare: str, file_name: str, encoding="latin-1") -> str:
    """
    Compare un hash MD5 à une liste de mots de passe
    :param hash_to_compare: le hash à retrouver
    :param file_name: le fichier contenant les mots de passe
    :param encoding: l'encodage du fichier
    :return: le mot de passe correspondant au hash
    """
    for password in open(file_name, "r", encoding=encoding):
        if hash_to_compare == text_to_md5(password.strip()):
            return password.strip()
    return ""


def find_hash_in_file(hash: str, file_name: str) -> None:
    """
    Recherche un hash dans une liste de mots de passe avec retours d'informations
    :param hash: le hash à retrouver
    :param file_name: le fichier contenant les mots de passe
    """
    print(f"Recherche du mot de passe correspondant au hash \"{hash}\" dans le fichier \"{file_name}\"...")
    timer_start = time.time()
    password = compare_md5_hash_to_file(hash, file_name)
    timer_end = time.time()

    if password != "":
        print(f"Le mot de passe est : {password}")
        print(f"Temps d'exécution : {round(timer_end - timer_start, 2)} secondes")
    else:
        print("Le mot de passe n'a pas été trouvé...")


def write_line_in_file(line: str, file_name="hashlist", encoding="utf-8") -> None:
    """
    Enregistre une ligne dans un fichier
    :param line: la ligne à enregistrer
    :param file_name: le fichier contenant les mots de passe
    :param encoding: l'encodage du fichier
    """
    with open(file_name, "a", encoding=encoding) as file:
        file.write(line + "\n")


def register_hash() -> None:
    """
    Enregistre un hash dans un fichier
    """
    input_hash = ""

    while input_hash == "":
        input_hash = input("Entrez le Hash à enregistrer : ")

    print("Enregistrement du hash...")
    write_line_in_file(input_hash)
    print("Le hash a bien été enregistré")


if __name__ == "__main__":
    # Setup terminal menus
    main_title = "Comparaison MD5\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Retrouver un Hash", "Enregistrer un Hash", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)
    select_hash_back = False
    select_file_back = False

    while True:
        main_entry_index = main_menu.show()
        # Retrouver un Hash
        if main_entry_index == 0:
            while not select_hash_back:
                select_hash_title = "Retrouver un Hash\nChoisissez le Hash à retrouver dans la liste"
                select_hash_options = list(list_hash())
                select_hash_options.append(None)
                select_hash_options.append("Retour")
                select_hash_menu = TerminalMenu(select_hash_options, title=select_hash_title, cycle_cursor=True,
                                                clear_screen=True)
                select_hash_entry_index = select_hash_menu.show()
                # Retour
                if select_hash_entry_index == len(select_hash_options) - 1 or select_hash_entry_index is None or \
                        select_hash_options[select_hash_entry_index] is None:
                    select_hash_back = True
                # Hash sélectionné
                else:
                    while not select_file_back:
                        select_file_title = "Retrouver un Hash\nChoisissez le fichier contenant les mots de passe à comparer"
                        select_file_options = list(list_text_files())
                        select_file_options.append(None)
                        select_file_options.append("Retour")
                        select_file_menu = TerminalMenu(select_file_options, title=select_file_title, cycle_cursor=True,
                                                        clear_screen=True)
                        select_file_entry_index = select_file_menu.show()
                        # Retour
                        if select_file_entry_index == len(select_file_options) - 1 or select_file_entry_index is None or \
                                select_file_options[select_file_entry_index] is None:
                            select_file_back = True
                        # Fichier sélectionné
                        else:
                            find_hash_in_file(select_hash_options[select_hash_entry_index],
                                              select_file_options[select_file_entry_index])
                            input("Appuyez sur Entrée pour continuer...")
                            select_file_back = True
                            select_hash_back = True
                    select_file_back = False
            select_hash_back = False
        # Enregistrer un Hash
        if main_entry_index == 1:
            register_hash()
            input("Appuyez sur Entrée pour continuer...")
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)
