
import numbers
import string
import numpy as np
import re
import collections


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
    '''
    Fonction permettant d'avoir tout les multiples d'un nombre
    :param number: Le nombre à analyser
    :return: L'ensemble des multiples et le nombre analysé
    '''
    half_number = number // 2
    all_multiple = []
    all_multiple.append(number)

    # On ajoute un car la boucle for exclu la valeur N
    for i in range(2, half_number + 1):
        if number % i == 0:
            all_multiple.append(i)

    return all_multiple


def findAllRepetitions (text: string, possible_length) :
    '''
    Fonction permettant de trouver toutes les répétitions possibles sans effectuer de tri
    :param text: Le texte à analyser
    :param possible_length: Objet stockant toutes les tailles possibles
    :return: Un objet contenant toutes les tailles possibles associés aux mots répétés
    '''
    length = len(text)
    start_number = 0
    last_start_number = 0
    end_number = 2
    last_word = ''

    while start_number < (length // 2) :
        if end_number < length // 2:
            end_number += 1

        if end_number > length // 2:
            break

        elif end_number == length // 2 :
            if start_number < length // 2:
                last_start_number += 1
                start_number = last_start_number + 1
                end_number = start_number + 2

        suite = text[start_number:end_number]

        if suite == last_word:
            continue

        nombre_rep = text.count(suite)

        if nombre_rep <= 1:
            start_number += 1
            continue
        else:
            all_occurence = []
            all_difference = []
            last_occurence = 0

            # Permet d'obtenir toutes les positions à laquelle la suite de lettre est répétée
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

            # Le décalage n'est pas identique partout, il ne faut pas pousser les valeurs.
            if len(set(all_difference)) != 1:
                start_number += 1
                continue

            all_multiples = get_all_multiple(all_difference[0])
            possible_length[suite] = all_multiples

            possible_length = delete_useless_data(suite, possible_length)

            start_number += 1

    return possible_length

def delete_useless_data(suite, possible_length):
    '''
    Fonction permettant de supprimer des valeurs inutiles
    :param suite: La suite de caractères
    :param possible_length: Le tableau contenant les différentes tailles possibles
    :return: Retourne le tableau sans doublon
    '''

    data_to_delete = []
    for property in possible_length:
        if property != suite and len(property) != len(suite):
            if property.startswith(suite) or suite.startswith(property) or suite.endswith(property) or property.endswith(suite):
                if len(property) > len(suite):
                    data_to_delete.append(suite)
                else:
                    data_to_delete.append(property)

    for property in data_to_delete:
        if property in possible_length:
            del possible_length[property]

    return possible_length


def refineMultiple (object) :
    '''
    Fonction permettant d'affiner les choix selectionnables par l'utilisateur
    :param object: L'objet contenant toutes les répétitions
    :return: Retourne l'ensemble des tailles possibles
    '''
    print('Voici pour chaque suite les multiples pouvant définir la taille de la clé: ', object)
    print('Un second traitement arrive pour afiner les résultats...')

    if len(object) == 0:
        print('Aucune suite ne se répète, nous ne pouvons pas trouver la longueur de la clé')
        return []
    elif len(object) == 1:
        first_key = list(object.keys())[0]
        print('Les possibilités sont: ', object[first_key])
        return object[first_key]
    elif len(object) > 1:
        all_values = []
        for property in object:
            for value in object[property]:
                all_values.append(value)

        most_frequent_multiple = collections.Counter(all_values).most_common()[0][1]
        if most_frequent_multiple != len(object):
            print('Aucun multiple est présent pour chacunes des chaines se répétant')
            most_frequent_multiple = collections.Counter(all_values).most_common(int(len(set(all_values)) * 0.10))
            multiple_without_repetitions = []
            for element in most_frequent_multiple:
                multiple_without_repetitions.append(element[0])
            print('Les multiples qui apparaissent 10% de fois plus que les autres sont : ', multiple_without_repetitions)
            return multiple_without_repetitions
        else:
            most_frequent_multiple = collections.Counter(all_values).most_common()[0][0]
            print('La clé est de la taille : ', most_frequent_multiple)
            return most_frequent_multiple

def divide_text (text):
    possible_length = {}
    all_position = findAllRepetitions(text, possible_length)
    all_length = refineMultiple(all_position)
    print(all_length)
    if len(all_length) != 0:
        for number in all_length:
            print(number)
            group = re.findall(f'.{{1,{number}}}', text)
            for i, char in enumerate(text):
                group[i % number] += char

            print(group)

if __name__ == "__main__":
    choice = input('Souhaitez vous chiffrer ou dechiffrer un message ? (réponse possible : cypher et decipher) ')

    if choice == 'cypher':
        cypher_message = vigenere_cypher()
        print('Message chiffré: ', cypher_message)
    elif choice == 'decipher':
        decipher_message = vigenere_decipher()
        print('Message déchiffré: ', decipher_message)
    elif choice == 'kasiski':
        possible_length = {}
        all_position = findAllRepetitions('MFUVAHGUTSGVMFUGUJPPEQTQSOUCIFP',  possible_length)
        refineMultiple(all_position)
    elif choice == 'cryptanalyse':
        divide_text('MFUVAHGUTSGVMFUTUJPPEQTQSOUCIFP')
    else:
        print()