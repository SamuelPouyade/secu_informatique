## Convertir le message en chiffre, le mettre entre 0 et 25
## Convertir la clé de chiffrement en chiffre et la mettre entre 0 et 25
## Additionner les deux chiffres et faire en sortes qu'ils soient compris entre 0 et 25

import numbers
import string


def convert_letter_to_number(text: string):
    """
    :param text: the message to be encrypted
    :return: the encrypted message
    """

    upper_text = text.upper()
    positions = []

    for char in upper_text:
        alphabet_position = ord(char) - ord('A')
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            positions.append(alphabet_position)
        else:
            positions.append(alphabet_position)

    return positions


def vigenere_cypher():

    message = input('Entrez le texte à chiffrer: ')
    encryption_key = input('Entrez la clé à utiliser: ')

    message = convert_letter_to_number(message)

    position_of_letter_of_encryption_key = convert_letter_to_number(encryption_key)

    if len(message) > len(position_of_letter_of_encryption_key):
        multiplicator = (len(message) // len(position_of_letter_of_encryption_key)) + 1
        encryption_key = position_of_letter_of_encryption_key * multiplicator


    counter = 0
    final_position = []
    cypher_message = []

    for position in message:
        if position < 0 or position > 25:
            final_position.append(position)
            counter += 1
        else:
            final_position.append((position + encryption_key[counter]) % 26)
            counter += 1

    for position in final_position:
        cypher_message.append(chr(ord('A') + position))

    return ''.join(cypher_message)


def vigenere_decipher():

    message = input('Entrez le texte à déchiffrer: ')
    decipher_key = input('Entrez la clé à utiliser: ')

    message = convert_letter_to_number(message)

    position_of_letter_of_encryption_key = convert_letter_to_number(decipher_key)

    if len(message) > len(position_of_letter_of_encryption_key):
        multiplicator = (len(message) // len(position_of_letter_of_encryption_key)) + 1
        decipher_key = position_of_letter_of_encryption_key * multiplicator

    counter = 0
    final_position = []
    decipher_message = []

    for position in message:
        if position < 0 or position > 25:
            final_position.append(position)
            counter += 1
        else:
            final_position.append((position - decipher_key[counter]) % 26)
            counter += 1

    for position in final_position:
        decipher_message.append(chr(ord('A') + position))

    return ''.join(decipher_message)


if __name__ == "__main__":
    choice = input('Souhaitez vous chiffrer ou dechiffrer un message ? (réponse possible : cypher et decipher) ')

    if choice == 'cypher':
        cypher_message = vigenere_cypher()
        print('Message chiffré: ', cypher_message)
    elif choice == 'decipher':
        decipher_message = vigenere_decipher()
        print('Message déchiffré: ', decipher_message)
    else:
        print()