
import numbers
import string
import numpy as np


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

def get_all_multiple (number: int):
    half_number = number // 2
    all_multiple = []
    all_multiple.append(number)

    # On ajoute un car la boucle for exclu la valeur N
    for i in range(2, half_number + 1):
        if number % i == 0:
            all_multiple.append(i)

    return all_multiple


def findAllRepetitions (text: string, nombre_depart_actuel: int, nombre_depart_precedent: int, nombre_arrive: int, taille_possible, mot_precedent: string) :
    length = len(text)

    if nombre_depart_actuel >= length or nombre_arrive > length:
        return taille_possible

    if nombre_arrive == length // 2 :
        if nombre_depart_actuel < length // 2:
            nombre_depart_actuel += nombre_depart_precedent + 1
            nombre_arrive = nombre_depart_actuel + 2

    suite = text[nombre_depart_actuel:nombre_arrive]

    if nombre_arrive > length // 2:
        return taille_possible

    if suite == mot_precedent:
        return taille_possible

    nombre_rep = text.count(suite)

    if nombre_rep <= 1:
        return findAllRepetitions(text, nombre_depart_actuel, nombre_depart_precedent, nombre_arrive+1, taille_possible, suite)
    else:
        all_occurence = []
        all_difference = []
        last_occurence = 0

        for i in range(nombre_rep):
            position = text.find(suite, last_occurence)
            all_occurence.append(position)
            # On augmente de 1 juste pour avoir un décalage et trouver la seconde position.
            last_occurence = position + 1

        for i in range(len(all_occurence) - 1):
            if all_occurence[i] == 0 :
                all_difference.append(all_occurence[i + 1])
            else:
                all_difference.append(all_occurence[i+1] - all_occurence[i])


        all_multiples = get_all_multiple(all_difference[0])
        taille_possible[suite] = all_multiples
        dataToDelete = []

        for property in taille_possible:
            if property != suite:
                if suite > property:
                    if suite.startswith(property):
                        dataToDelete.append(property)
                elif property > suite:
                    if property.startswith(suite):
                        dataToDelete.append(suite)

        for property in dataToDelete:
            del taille_possible[property]

        return findAllRepetitions(text, nombre_depart_actuel, nombre_depart_precedent + 1, nombre_arrive + 1, taille_possible, suite)

def refineMultiple (object) :
    all_posibilities = []
    for property in object:
        for property2 in object:
            if property != property2:
                if set(object[property]) & set(object[property2]):
                    if object[property] not in all_posibilities:
                        all_posibilities.append(object[property])

    tableau_applati = np.array(all_posibilities).flatten().tolist()

    print('La clé peut être égale à une taille de ces numéros suivant : ', set(tableau_applati))

if __name__ == "__main__":
    choice = input('Souhaitez vous chiffrer ou dechiffrer un message ? (réponse possible : cypher et decipher) ')

    if choice == 'cypher':
        cypher_message = vigenere_cypher()
        print('Message chiffré: ', cypher_message)
    elif choice == 'decipher':
        decipher_message = vigenere_decipher()
        print('Message déchiffré: ', decipher_message)
    elif choice == 'findAllRepetitions':
        taille_possible = {}
        all_position = findAllRepetitions('MFUVAIHGUOTVAIMFUTUJPIIPETQSOUCPIFP', 0, 0, 2,  taille_possible, '')
        refineMultiple(all_position)
    else:
        print()