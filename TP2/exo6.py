from PIL import Image
import os

from simple_term_menu import TerminalMenu

def calculate_XOR(nombreDepart: int, cle: int) -> int:
    """
    Applique le XOR entre un byte et un élément de la clé.
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

            with open(f"decrypted_file_simple{i}.jpg", "wb") as decrypted_file:
                decrypted_file.write(bytes(decrypted_data))

            try:
                with Image.open(f"decrypted_file_simple{i}.jpg") as img:
                    img.verify()
                print(f"L'image déchiffrée {f"decrypted_file_simple{i}.jpg"} est valide.")
                break
            except (IOError, SyntaxError) as e:
                os.remove(f"decrypted_file_simple{i}.jpg")


def calculer_cle_xor():
    with open('encrypted_file_hard.jpg', "rb") as encrypted_file:
        header_chiffre = encrypted_file.read(25)

    with open('téléchargement.jpeg', "rb") as file:
        header = file.read(25)
        print(header)

    cle_xor = bytearray()
    for byte_chiffre, byte_attendu in zip(header_chiffre, header):
        cle_xor.append(byte_chiffre ^ byte_attendu)

    return cle_xor

def find_repeated_sequences_max_half_length(numbers):
    repeated_sequences = {}
    max_length = len(numbers)

    for length in range(1, max_length + 1):
        for i in range(len(numbers) - length):
            suite = numbers[i:i + length]
            repeated_sequences[tuple(suite)] = 1

    return repeated_sequences


def apply_cyclic_XOR(encrypted_data, key):
    """
    Applique le XOR cyclique avec la clé sur les données chiffrées.
    """
    decrypted_data = []
    key_length = len(key)

    for i, byte in enumerate(encrypted_data):
        decrypted_byte = byte ^ key[i % key_length]
        decrypted_data.append(decrypted_byte)

    return decrypted_data

def decipher_hard_XOR():
    """
    Déchiffre une image chiffrée avec la clé XOR calculée.
    """
    # Charger l'image chiffrée
    with open("encrypted_file_hard.jpg", "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Calculer la clé XOR
    key = [132, 12, 73, 26, 152, 130, 82, 186, 31, 148, 36, 21, 196, 203, 15, 4]

    # Appliquer le XOR avec la clé de manière cyclique
    decrypted_data = apply_cyclic_XOR(encrypted_data, key)

    # Sauvegarder l'image déchiffrée
    output_file = "decrypted_file_hard.jpg"
    with open(output_file, "wb") as decrypted_file:
        decrypted_file.write(bytes(decrypted_data))

    # Vérifier si l'image est valide
    try:
        with Image.open(output_file) as img:
            img.verify()
        print(f"L'image déchiffrée {output_file} est valide.")
    except (IOError, SyntaxError):
        print(f"L'image déchiffrée {output_file} est invalide.")
        os.remove(output_file)

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
            all_key = calculer_cle_xor()
            all_sequence = find_repeated_sequences_max_half_length(all_key)
            decipher_hard_XOR()
            await_input()
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)





