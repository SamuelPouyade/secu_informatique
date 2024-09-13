from simple_term_menu import TerminalMenu


def cesar_cipher(text: str, offset: int, encrypt=True) -> str:
    """
    Fonction permettant de chiffrer ou de déchiffrer un message en utilisant le chiffrement de César
    :param text: le message à traiter
    :param offset: valeur de décalage
    :param encrypt: chiffrement (True par défaut) ou déchiffrement (False)
    :return: le message traité
    """

    # Conversion du texte en majuscule pour uniformiser les codes ASCII
    upper_text = text.upper()

    # Variable qui stock le message chiffré
    processed_text = []

    for char in upper_text:
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            # Le caractère n'est pas une lettre de l'alphabet
            processed_text.append(char)
        else:
            alphabet_position = ord(char) - ord('A')
            if encrypt:
                position = (alphabet_position + offset) % 26
            else:
                position = (alphabet_position - offset) % 26
            processed_text.append(chr(ord('A') + position))

    return "".join(processed_text)


if __name__ == "__main__":
    # Setup du menu
    main_title = "Chiffrement de César\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Chiffrement", "Déchiffrement", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)

    decryption_title = "Déchiffrement\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    decryption_options = ["Déchiffrer", "Attaque \"Brute force\"", None, "Retour"]
    decryption_menu = TerminalMenu(decryption_options, title=decryption_title, cycle_cursor=True, clear_screen=True)
    decryption_menu_back = False

    while True:
        main_entry_index = main_menu.show()
        # Chiffrement
        if main_entry_index == 0:
            input_text = input('Entrez le message à chiffrer: ')
            while True:
                try:
                    input_offset = int(input('Saisissez la taille du décalage: '))
                    break
                except ValueError:
                    print("Veuillez saisir un nombre entier")
            cypher_message = cesar_cipher(input_text, input_offset)
            print('Message chiffré: %s' % cypher_message)
            input('Appuyez sur Entrée pour continuer...')
        # Déchiffrement
        elif main_entry_index == 1:
            while not decryption_menu_back:
                decryption_entry_index = decryption_menu.show()
                # Déchiffrer
                if decryption_entry_index == 0:
                    input_text = input('Entrez le message à déchiffrer: ')
                    while True:
                        try:
                            input_offset = int(input('Saisissez la taille du décalage: '))
                            break
                        except ValueError:
                            print("Veuillez saisir un nombre entier")
                    decipher_message = cesar_cipher(input_text, input_offset, False)
                    print('Message déchiffré: %s' % decipher_message)
                    input('Appuyez sur Entrée pour continuer...')
                    decryption_menu_back = True
                # Attaque "Brute force"
                elif decryption_entry_index == 1:
                    input_text = input('Entrez le message à déchiffrer: ')
                    print("Liste des messages déchiffrés pour chaque décalage possible: ")
                    for i in range(25):
                        decipher_message = cesar_cipher(input_text, i + 1, False)
                        print(decipher_message)
                    input('Appuyez sur Entrée pour continuer...')
                    decryption_menu_back = True
                # Retour
                if decryption_entry_index == len(decryption_options) - 1:
                    decryption_menu_back = True
            decryption_menu_back = False
        # Quitter
        elif main_entry_index == len(main_options) - 1:
            print("Au revoir !")
            exit(0)
