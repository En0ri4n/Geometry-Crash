def main():
    str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    list = []
    for i in range(0, 26):
        list.append(str[i])

    print(list)


if __name__ == '__main__':
    main()


def decode():
    key = input("Insert Word Key :").upper()
    coded_word = input("Insert Coded Word :").upper()

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']

    z = []
    for i in range(0, len(coded_word)):
        z.append(alphabet.index(coded_word[i]))

    y = []
    key_index = 0
    for i in range(0, len(coded_word)):
        y.append(alphabet.index(key[key_index]))
        if key_index + 1 >= len(key):
            key_index = 0
        else:
            key_index += 1

    decoded_word = ""
    letter_index = 0
    for i in range(0, len(coded_word)):
        letter_index = z[i] - y[i]
        decoded_word += alphabet[letter_index]

    print("Y : " + str(y))
    print("Z : " + str(z))
    print("Decoded Word : " + decoded_word)

    decoded_map = []
    for i in range(0, len(decoded_word)):
        decoded_map.append(decoded_word[i] + "=" + str(alphabet.index(decoded_word[i])))

    print("Decoded Map (x) : " + str(decoded_map))


def encode():
    key = input("Insert Word Key :").upper()
    uncoded_word = input("Insert Word To Encode :").upper()

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']

    x = []
    for i in range(0, len(uncoded_word)):
        x.append(alphabet.index(uncoded_word[i]))

    y = []
    key_index = 0
    for i in range(0, len(uncoded_word)):
        y.append(alphabet.index(key[key_index]))
        if key_index + 1 >= len(key):
            key_index = 0
        else:
            key_index += 1

    encoded_word = ""
    letter_index = 0
    for i in range(0, len(uncoded_word)):
        letter_index = x[i] + y[i]
        while letter_index >= len(alphabet):
            letter_index -= 26
        encoded_word += str(alphabet[letter_index])

    print("X : " + str(x))
    print("Y : " + str(y))
    print("Encoded Word : " + encoded_word)

    encoded_map = []
    for i in range(0, len(encoded_word)):
        encoded_map.append(encoded_word[i] + "=" + str(alphabet.index(encoded_word[i])))

    print("Decoded Map (z) : " + str(encoded_map))
