import numbers
import string


def cesar_encryption(offset: numbers, text: string):
    """

    :param offset: the number of shifts
    :param text: the message to be encrypted
    :return: the encrypted message
    """

    upper_text = text.upper()
    positions = []
    cypher_message = []

    for char in upper_text:
        alphabet_position = ord(char) - ord('A')
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            positions.append(alphabet_position)
        else:
            positions.append((alphabet_position + offset) % 26)

    for position in positions:
        cypher_message.append(chr(ord('A') + position))

    return ''.join(cypher_message)


def cesar_decipher(offset: numbers, text: string):
    """
        :param offset: the number of shifts
        :param text: the message to be deciphered
        :return: the deciphered message
    """
    upper_text = text.upper()
    positions = []
    decipher_message = []

    for char in upper_text:
        alphabet_position = ord(char) - ord('A')
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            positions.append(alphabet_position)
        else:
            positions.append((alphabet_position - offset) % 26)

    for position in positions:
        decipher_message.append(chr(ord('A') + position))

    return ''.join(decipher_message)


if __name__ == "__main__":
    OFFSET = 12
    TEXT = "mec super cool!! 1111 <>?(*)^%$^%^#&*%^"

    cypher_message = cesar_encryption(OFFSET, TEXT)
    print('message chiffré: %s' % cypher_message)

    decipher_message = cesar_decipher(OFFSET, cypher_message)
    print('message déchiffré: %s' % decipher_message)

    print('Seconde partie: ')
    for i in range(25):
        decipher_message = cesar_decipher(i+1, cypher_message)
        print('message déchiffré: %s' % decipher_message)