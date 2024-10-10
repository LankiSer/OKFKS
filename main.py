import streamlit as st
import string
import random

# Функция для шифра Цезаря
def caesar_cipher(text, shift, encrypt=True):
    result = ""
    for char in text:
        if char.isalpha():
            if 'А' <= char <= 'Я' or 'а' <= char <= 'я':  # Русский алфавит
                shift_direction = shift if encrypt else -shift
                offset = 1040 if char.isupper() else 1072  # Кодировка для 'А' и 'а'
                result += chr((ord(char) - offset + shift_direction) % 33 + offset)
            else:  # Латинский алфавит
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
        if 'А' <= char <= 'Я':  # Русский заглавный алфавит
            result += chr(1040 + (32 - (ord(char) - 1040)))
        elif 'а' <= char <= 'я':  # Русский строчный алфавит
            result += chr(1072 + (32 - (ord(char) - 1072)))
        elif 'A' <= char <= 'Z':  # Латинский заглавный алфавит
            result += chr(65 + (25 - (ord(char) - 65)))
        elif 'a' <= char <= 'z':  # Латинский строчный алфавит
            result += chr(97 + (25 - (ord(char) - 97)))
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
            if 'А' <= char <= 'Я' or 'а' <= char <= 'я':  # Русский алфавит
                shift = (ord(key[key_index % len(key)]) - 1072) % 33
                if not encrypt:
                    shift = -shift
                offset = 1040 if char.isupper() else 1072
                result += chr((ord(char) - offset + shift) % 33 + offset)
                key_index += 1
            elif 'A' <= char <= 'Z' or 'a' <= char <= 'z':  # Латинский алфавит
                shift = (ord(key[key_index % len(key)]) - ord('a')) % 26
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
    key = key.lower().replace('ё', 'е')  # Заменяем 'ё' на 'е'
    key = ''.join(sorted(set(key), key=key.index))  # Убираем повторяющиеся символы из ключа
    alphabet = "абвгдежзийклмнопрстуфхцчшщьыъэюя".replace('ё', 'е')  # Русский алфавит без 'ё'

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

    # Формируем 6x6 матрицу
    return [matrix[i:i + 6] for i in range(0, 36, 6)]

def find_position(matrix, char):
    for row in range(6):
        for col in range(6):
            if matrix[row][col] == char:
                return row, col
    return None

def playfair_cipher(text, key, encrypt=True):
    text = text.lower().replace('ё', 'е')  # Заменяем 'ё' на 'е'
    text = text.replace(' ', '')  # Убираем пробелы

    # Удаляем из текста символы, которые не являются буквами русского алфавита
    alphabet = "абвгдежзийклмнопрстуфхцчшщьыъэюя"
    text = ''.join([char for char in text if char in alphabet])

    matrix = generate_playfair_matrix(key)

    # Разбиваем текст на биграммы
    bigrams = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'х'  # Добавляем 'х', если нечётное количество букв
        if a == b:
            b = 'х'  # Если буквы одинаковы, добавляем 'х'
        bigrams.append((a, b))
        i += 2

    result = []
    for a, b in bigrams:
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            # Если обе буквы в одной строке, сдвигаем их вправо (или влево при дешифровке)
            if encrypt:
                result.append(matrix[row_a][(col_a + 1) % 6])
                result.append(matrix[row_b][(col_b + 1) % 6])
            else:
                result.append(matrix[row_a][(col_a - 1) % 6])
                result.append(matrix[row_b][(col_b - 1) % 6])
        elif col_a == col_b:
            # Если обе буквы в одном столбце, сдвигаем их вниз (или вверх при дешифровке)
            if encrypt:
                result.append(matrix[(row_a + 1) % 6][col_a])
                result.append(matrix[(row_b + 1) % 6][col_b])
            else:
                result.append(matrix[(row_a - 1) % 6][col_a])
                result.append(matrix[(row_b - 1) % 6][col_b])
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
        
# Инициализация состояния
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ""
if 'output_text' not in st.session_state:
    st.session_state['output_text'] = ""
if 'key' not in st.session_state:
    st.session_state['key'] = "ключ"  # Значение по умолчанию для Виженера
if 'key2' not in st.session_state:
    st.session_state['key2'] = "ключ"  # Значение по умолчанию для Плейфера

# Интерфейс Streamlit
st.title('Шифраторы')

# Выбор шифратора
cipher_choice = st.selectbox(
    "Выберите шифратор",
    ["Цезарь", "Атбаш", "Виженер", "Плейфер", "RSA"]
)

# Поля для ввода текста и результат
input_text = st.text_area("Введите текст", value=st.session_state.input_text, height=200, key="input_text_area")
output_text = ""

# Поля для дополнительных параметров (например, сдвиг или ключ)
if cipher_choice == "Цезарь":
    shift = st.slider("Сдвиг", min_value=1, max_value=25, value=3, key="caesar_shift")
elif cipher_choice == "Виженер":
    key = st.text_input("Ключевое слово", value=st.session_state.key, key="vigenere_key")
elif cipher_choice == "Плейфер":
    key2 = st.text_input("Ключевое слово", value=st.session_state.key2, key="playfair_key")

# Генерация и хранение ключей для RSA
if cipher_choice == "RSA":
    if 'public_key' not in st.session_state:
        public_key, private_key = generate_rsa_keypair()
        st.session_state['public_key'] = public_key
        st.session_state['private_key'] = private_key
    else:
        public_key = st.session_state['public_key']
        private_key = st.session_state['private_key']

# Кнопки
col1, col2, col3 = st.columns(3)

# Обработка кнопки "Зашифровать"
with col1:
    if st.button("Зашифровать"):
        if cipher_choice == "Цезарь":
            st.session_state.output_text = caesar_cipher(input_text, shift, encrypt=True)
        elif cipher_choice == "Атбаш":
            st.session_state.output_text = atbash_cipher(input_text)
        elif cipher_choice == "Виженер":
            st.session_state.output_text = vigenere_cipher(input_text, key, encrypt=True)
        elif cipher_choice == "Плейфер":
            st.session_state.output_text = playfair_cipher(input_text, key2, encrypt=True)
        elif cipher_choice == "RSA":
            st.session_state.output_text = rsa_encrypt(input_text, public_key)

# Обработка кнопки "Расшифровать"
with col2:
    if st.button("Расшифровать"):
        if cipher_choice == "Цезарь":
            st.session_state.output_text = caesar_cipher(input_text, shift, encrypt=False)
        elif cipher_choice == "Атбаш":
            st.session_state.output_text = atbash_cipher(input_text)  # Симметричный шифр
        elif cipher_choice == "Виженер":
            st.session_state.output_text = vigenere_cipher(input_text, key, encrypt=False)
        elif cipher_choice == "Плейфер":
            st.session_state.output_text = playfair_cipher(input_text, key2, encrypt=False)
        elif cipher_choice == "RSA":
            try:
                cipher_text = list(map(int, input_text.split()))  # Преобразуем строку обратно в числа
                st.session_state.output_text = rsa_decrypt(cipher_text, private_key)
            except ValueError:
                st.session_state.output_text = "Ошибка при дешифровке RSA. Проверьте зашифрованный текст."

with col3:
    if st.button("Скопировать"):
        # Копируем результат в поле ввода (перемещаем вывод в ввод)
        st.session_state['input_text'] = st.session_state['output_text']
        st.experimental_rerun()  # Перезагрузка интерфейса для обновления поля ввода   
        
    if st.button("Очистить"):
        # Очищаем оба поля
        st.session_state['input_text'] = ""
        st.session_state['output_text'] = ""
        st.experimental_rerun()  # Перезагрузка




# Вывод результата в текстовое поле (заблокированное для редактирования)
st.text_area("Результат", value=st.session_state.output_text, height=200, key="output_text_area", disabled=True)
