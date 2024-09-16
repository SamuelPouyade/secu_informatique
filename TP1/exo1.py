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


def cipher_input(encrypt=True) -> None:
    """
    Fonction permettant la saisie utilisateur d'un message dans le terminal et procède au chiffrement ou déchiffrement
    du message à l'aide du chiffrement de César
    :param encrypt: chiffrement (True par défaut) ou déchiffrement (False)
    :return: Le message chiffré ou déchiffré dans le terminal
    """

    input_text = ""

    # Le message ne doit pas être vide
    while input_text == "":
        input_text = input(f"Entrez le message à {"chiffrer" if encrypt else "déchiffrer"} : ")

    # Le décalage doit être un nombre entier positif
    while True:
        try:
            input_offset = int(input("Saisissez la taille du décalage : "))
            if input_offset <= 0:
                print("Veuillez saisir un nombre entier positif supérieur à 0")
                continue
            break
        except ValueError:
            print("Veuillez saisir un nombre entier")

    cypher_message = cesar_cipher(input_text, input_offset, encrypt)

    print(f"Message {"chiffré" if encrypt else "déchiffré"} : {cypher_message}")


def cipher_brute_force_input() -> None:
    """
    Fonction permettant la saisie utilisateur d'un message chiffré avec le chiffrement de César dans le terminal et
    procède à une attaque "Brute force" du message
    :return: La liste des messages déchiffrés pour chaque décalage possible dans le terminal
    """

    input_text = ""

    # Le message ne doit pas être vide
    while input_text == "":
        input_text = input("Entrez le message à déchiffrer : ")

    print("Liste des messages déchiffrés pour chaque décalage possible : ")
    for i in range(25):
        decipher_message = cesar_cipher(input_text, i + 1, False)
        print(decipher_message)


def await_input() -> None:
    """
    Fonction permettant d'attendre une saisie utilisateur pour continuer
    :return: None
    """

    input("Appuyez sur Entrée pour continuer...")


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
            cipher_input(True)
            await_input()
        # Déchiffrement
        elif main_entry_index == 1:
            while not decryption_menu_back:
                decryption_entry_index = decryption_menu.show()
                # Déchiffrer
                if decryption_entry_index == 0:
                    cipher_input(False)
                    await_input()
                    decryption_menu_back = True
                # Attaque "Brute force"
                elif decryption_entry_index == 1:
                    cipher_brute_force_input()
                    await_input()
                    decryption_menu_back = True
                # Retour
                if decryption_entry_index == len(decryption_options) - 1:
                    decryption_menu_back = True
            decryption_menu_back = False
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)
