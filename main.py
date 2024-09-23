import streamlit as st
import string
import random


# Функция для шифра Цезаря
def caesar_cipher(text, shift, encrypt=True):
    result = ""
    for char in text:
        if char.isalpha():
            shift_direction = shift if encrypt else -shift
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift_direction) % 26 + offset)
        else:
            result += char
    return result


# Функция для шифра Атбаш
def atbash_cipher(text):
    result = ""
    for char in text:
        if char.isalpha():  # Проверяем, является ли символ буквой
            offset = 65 if char.isupper() else 97  # Определяем, заглавная или строчная буква
            result += chr(25 - (ord(char) - offset) + offset)  # Применяем шифр Атбаш
        else:
            result += char  # Оставляем любой другой символ как есть
    return result


# Функция для шифра Виженера
def vigenere_cipher(text, key, encrypt=True):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if not encrypt:
                shift = -shift
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
            key_index += 1
        else:
            result += char
    return result


# Функция для шифра Плейфера
def generate_playfair_matrix(key):
    key = ''.join(sorted(set(key), key=key.index))
    alphabet = string.ascii_lowercase.replace('j', '')  # Убираем букву 'j'
    matrix = []
    used_letters = set()

    # Сначала добавляем ключ
    for char in key:
        if char not in used_letters and char.isalpha():
            matrix.append(char)
            used_letters.add(char)

    # Потом добавляем оставшиеся буквы алфавита
    for char in alphabet:
        if char not in used_letters:
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None


def playfair_cipher(text, key, encrypt=True):
    text = text.replace(' ', '').lower()
    text = text.replace('j', 'i')  # Заменяем 'j' на 'i'
    matrix = generate_playfair_matrix(key)

    # Разбиваем текст на биграммы
    bigrams = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'x'  # Добавляем 'x', если нечётное количество букв
        if a == b:
            b = 'x'  # Если буквы одинаковы в биграмме, добавляем 'x'
        bigrams.append((a, b))
        i += 2

    result = []
    for a, b in bigrams:
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            # Если обе буквы в одной строке, сдвигаем их вправо (или влево при дешифровке)
            if encrypt:
                result.append(matrix[row_a][(col_a + 1) % 5])
                result.append(matrix[row_b][(col_b + 1) % 5])
            else:
                result.append(matrix[row_a][(col_a - 1) % 5])
                result.append(matrix[row_b][(col_b - 1) % 5])
        elif col_a == col_b:
        # Если обе буквы в одном столбце, сдвигаем их вниз (или вверх при дешифровке)
            if encrypt:
                result.append(matrix[(row_a + 1) % 5][col_a])
                result.append(matrix[(row_b + 1) % 5][col_b])
            else:
                result.append(matrix[(row_a - 1) % 5][col_a])
                result.append(matrix[(row_b - 1) % 5][col_b])
        else:
        # Если буквы находятся в разных строках и столбцах, заменяем их на буквы в углах прямоугольника
            result.append(matrix[row_a][col_b])
            result.append(matrix[row_b][col_a])

    return ''.join(result)

# Заглушка для шифра RSA (упрощенная версия)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Функция для нахождения мультипликативного обратного числа
def mod_inverse(e, phi):
    old_r, r = phi, e
    old_s, s = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if old_s < 0:
        old_s += phi
    return old_s

# Функция для генерации больших случайных простых чисел (для демонстрации)
def generate_large_prime():
    while True:
        num = random.randint(1000, 5000)  # Это пример, в реальной системе числа должны быть намного больше
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            return num

# Генерация ключа RSA
def generate_rsa_keypair():
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбираем число e, которое является взаимно простым с phi(n)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # Вычисляем закрытый ключ d
    d = mod_inverse(e, phi)

    # Публичный и приватный ключи
    return ((e, n), (d, n))

# Функция шифрования с использованием открытого ключа
def rsa_encrypt(text, public_key):
    e, n = public_key
    cipher = [(ord(char) ** e) % n for char in text]
    return cipher

# Функция дешифрования с использованием закрытого ключа
def rsa_decrypt(cipher, private_key):
    d, n = private_key
    plain = [(char ** d) % n for char in cipher]

    # Преобразуем обратно в символы, если это возможно
    try:
        return ''.join([chr(char) for char in plain])
    except ValueError:
        # Если символы выходят за пределы допустимого диапазона chr(), возвращаем байтовое представление
        return ''.join([str(char) for char in plain])

# Интерфейс Streamlit
st.title('Шифраторы')

# Выбор шифратора
cipher_choice = st.selectbox(
    "Выберите шифратор",
    ["Цезарь", "Атбаш", "Виженер", "Плейфер", "RSA"]
)

# Поля для ввода текста и результата
input_text = st.text_area("Введите текст", height=200, key="input_text")
output_text = ""

# Поля для дополнительных параметров (например, сдвиг или ключ)
if cipher_choice == "Цезарь":
    shift = st.slider("Сдвиг", min_value=1, max_value=25, value=3)
elif cipher_choice == "Виженер":
    key = st.text_input("Ключевое слово", value="ключ", key="vigenere_key")

# Генерация и хранение ключей для RSA
if cipher_choice == "RSA":
    public_key, private_key = generate_rsa_keypair()

# Кнопки
col1, col2 = st.columns(2)

# Обработка кнопки "Зашифровать"
with col1:
    if st.button("Зашифровать"):
        if cipher_choice == "Цезарь":
            output_text = caesar_cipher(input_text, shift, encrypt=True)
        elif cipher_choice == "Атбаш":
            output_text = atbash_cipher(input_text)
        elif cipher_choice == "Виженер":
            output_text = vigenere_cipher(input_text, key, encrypt=True)
        elif cipher_choice == "Плейфер":
            output_text = playfair_cipher(input_text, key="ключ", encrypt=True)
        elif cipher_choice == "RSA":
            output_text = rsa_encrypt(input_text, public_key)

# Обработка кнопки "Расшифровать"
with col2:
    if st.button("Расшифровать"):
        if cipher_choice == "Цезарь":
            output_text = caesar_cipher(input_text, shift, encrypt=False)
        elif cipher_choice == "Атбаш":
            output_text = atbash_cipher(input_text)  # Шифр Атбаш симметричный, шифрование и дешифрование одинаково
        elif cipher_choice == "Виженер":
            output_text = vigenere_cipher(input_text, key, encrypt=False)  # Для дешифровки используем encrypt=False
        elif cipher_choice == "Плейфер":
            output_text = playfair_cipher(input_text, key="ключ",
                                          encrypt=False)  # Для дешифровки используем encrypt=False
        elif cipher_choice == "RSA":
            try:
                # Пытаемся расшифровать текст, если он был зашифрован с помощью RSA
                cipher_text = list(map(int, input_text.split()))  # Преобразуем строку обратно в числа
                output_text = rsa_decrypt(cipher_text, private_key)
            except ValueError:
                output_text = "Ошибка при дешифровке RSA. Проверьте зашифрованный текст."

# Вывод результата в текстовое поле (заблокированное для редактирования)
st.text_area("Результат", value=output_text, height=200, key="output_text", disabled=True)