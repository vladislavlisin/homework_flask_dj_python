# ЗАДАНИЯ ПО ЧИСТОМУ ПИТОНУ

def fuct(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    else:
        return n * fuct(n - 1)


def pascal_triangle(n: int) -> int:
    # number amount in a row
    for i in range(0, n + 1):
        C_i_k = [fuct(i) / (fuct(i - k) * fuct(k)) for k in range(0, i + 1)]
        print(C_i_k)

    return 0


def caesar_cipher(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif char.isupper():
                encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def check(s: str) -> bool:
   counter = 0
   for i in s:
     if i == '(':
       counter = counter + 1
     else:
       counter = counter - 1
     if counter < 0:
       return False
   return counter == 0


if __name__ == "__main__":


    # FIRST

    n = input()
    print(f"Вы ввели {n}")

    try:
        n = int(n)
        if n <= 0:
            print("Число должно быть больше 0")
        else:
            pascal_triangle(n)
    except ValueError:
        print("Вы ввели нецелое число")



    # SECOND

    string = "((())()()(()))"

    print(check(string))


    # THIRD



    path = "text.txt"
    shift = 3
    language = "english"

    # Чтение информации из файла
    with open(path, 'r') as file:
        text = file.readline().strip()

    # Шифрование текста
    encrypted_text = caesar_cipher(text, shift)

    # Запись зашифрованного текста в новый файл
    with open('output.txt', 'w') as output_file:
        output_file.write(encrypted_text)

    print("Текст успешно зашифрован и записан в файл output.txt")



