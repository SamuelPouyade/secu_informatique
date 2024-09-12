def cesar_cipher(offset: int, text: str, encrypt = True) -> str:
    """
    Fonction permettant de chiffrer un message en utilisant le chiffrement de César
    :param offset: valeur de décalage
    :param text: le message à chiffrer
    :param encrypt: chiffrement (True par défaut) ou déchiffrement (False)
    :return: le message chiffré
    """

    # Conversion du texte en majuscule pour uniformiser les codes ASCII
    upper_text = text.upper()

    # Variable qui stock le message chiffré
    processed_text = []

    for char in upper_text:
        alphabet_position = ord(char) - ord('A')
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            # Le caractère n'est pas une lettre de l'alphabet
            processed_text.append(alphabet_position)
        else:
            if encrypt:
                position = (alphabet_position + offset) % 26
            else:
                position = (alphabet_position - offset) % 26
            processed_text.append(chr(ord('A') + position))

    return "".join(processed_text)


if __name__ == "__main__":

    choice = input('Souhaitez vous chiffrer ou dechiffrer un message ? (réponse possible : cypher et decipher) ')

    if choice == 'cypher':
        TEXT = input('Entrez le message à chiffrer: ')
        OFFSET = int(input('Saisissez la taille du décalage: '))
        cypher_message = cesar_cipher(OFFSET, TEXT)
        print('message chiffré: %s' % cypher_message)
    elif choice == 'decipher':
        second_choice = input('Connaissez-vous le décalage ? (o ou n) ')
        if second_choice == 'o':
            OFFSET = int(input('Saisissez la taille du décalage: '))
            TEXT = input('Entrez le message à déchiffrer: ')
            decipher_message = cesar_cipher(OFFSET, TEXT, False)
            print('message déchiffré: %s' % decipher_message)
        elif second_choice == 'n':
            TEXT = input('Entrez le message à déchiffrer: ')
            for i in range(25):
                decipher_message = cesar_cipher(i + 1, TEXT, False)
                print('message déchiffré: %s' % decipher_message)
