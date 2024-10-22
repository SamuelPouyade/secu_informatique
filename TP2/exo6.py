from PIL import Image
import os
import string

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


def calculer_cle_xor(input_file: string):
    with open(input_file, "rb") as encrypted_file:
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
    if len(set(numbers)) == 1:
        repeated_sequences[tuple(numbers)] = 1
        return repeated_sequences

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

def decipher_hard_XOR(all_sequence, input_file, output_file):
    """
    Déchiffre une image chiffrée avec la clé XOR calculée.
    """
    with open(input_file, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    for sequence in all_sequence:
        key = tuple(sequence)
        decrypted_data = apply_cyclic_XOR(encrypted_data, key)

        with open(output_file, "wb") as decrypted_file:
            decrypted_file.write(bytes(decrypted_data))

        try:
            with Image.open(output_file) as img:
                img.verify()
            print(f"L'image déchiffrée {output_file} est valide.")
            break
        except (IOError, SyntaxError):
            print(f"L'image déchiffrée {output_file} est invalide.")
            os.remove(output_file)

if __name__ == "__main__":
    # Setup du menu
    main_title = "Cryptographie symètrique\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Déchiffrement simple", "Déchiffrement simple avancé", "Déchiffrement difficile", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)

    while True:
        main_entry_index = main_menu.show()
        # Déchiffrement simple
        if main_entry_index == 0:
            decipher_simple_XOR()
            await_input()
        # Déchiffrement simple avancé
        if main_entry_index == 1:
            input_file = "encrypted_file_simple.jpg"
            output_file = "decrypted_file_simple.jpg"
            all_key = calculer_cle_xor(input_file)
            all_sequence = find_repeated_sequences_max_half_length(all_key)
            decipher_hard_XOR(all_sequence, input_file, output_file)
            await_input()
        # Déchiffrement difficile
        elif main_entry_index == 2:
            input_file = "encrypted_file_hard.jpg"
            output_file = "decrypted_file_hard.jpg"
            all_key = calculer_cle_xor(input_file)
            all_sequence = find_repeated_sequences_max_half_length(all_key)
            decipher_hard_XOR(all_sequence, input_file, output_file)
            await_input()
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)





