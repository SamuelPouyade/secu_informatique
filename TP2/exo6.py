from PIL import Image
import os

from simple_term_menu import TerminalMenu

def calculate_XOR (nombreDepart: int, cle: int) -> bin:
    """
    Fonction permettant de calculer le XOR entre un byte de l'image et un byte au hasard parmis les 255 possibilités
    :param nombreDepart: Le nombre du départ
    :param cle: la clé potentiellement utilisée
    :return: le XOR
    """
    return nombreDepart ^ cle

def await_input() -> None:
    """
    Fonction permettant d'attendre une saisie utilisateur pour continuer
    :return: None
    """

    input("Appuyez sur Entrée pour continuer...")

def decipher_simple_XOR():
    """
    Fonction permettant d'ouvrir l'image chiffrée de manière simple en utilisant XOR
    :return: Ecrit une image ouvrable
    """
    with open("encrypted_file_simple.jpg", "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

        for i in range(256):
            decrypted_data = []
            for byte in encrypted_data:
                decrypted_data.append((calculate_XOR(byte, i)))

            decrypted_date = bytes(decrypted_data)

            with open(f"decrypted_file_simple{i}.jpg", "wb") as decrypted_file:
                decrypted_file.write(bytes(decrypted_data))

            try:
                with Image.open(f"decrypted_file_simple{i}.jpg") as img:
                    img.verify();
                print(f"L'image décryptée {f"decrypted_file_simple{i}.jpg"} est valide.")
            except (IOError, SyntaxError) as e:
                os.remove(f"decrypted_file_simple{i}.jpg")

if __name__ == "__main__":
    # Setup du menu
    main_title = "Cryptographie symètrique\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Déchiffrement simple", "Déchiffrement difficile", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)

    while True:
        main_entry_index = main_menu.show()
        # Chiffrement
        if main_entry_index == 0:
            decipher_simple_XOR()
            await_input()
        # Déchiffrement
        elif main_entry_index == 1:
           print("C'est dur !!!")
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)





