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

def vigenere_cypher(encryption_key:  list[int], message: list[int]):
    print(len(message))
    for positon in message:
        print(positon, encryption_key[1])

if __name__ == "__main__":
    ENCRYPTION_KEY = 'cle'
    TEXT = "za"

    position_of_letter_to_be_cypher = convert_letter_to_number(TEXT)
    print('message chiffré: %s' % position_of_letter_to_be_cypher)

    position_of_letter_of_encryption_key = convert_letter_to_number(ENCRYPTION_KEY)
    print('message chiffré: %s' % position_of_letter_of_encryption_key)

    vigenere_cypher(position_of_letter_of_encryption_key, position_of_letter_to_be_cypher)
