import subprocess
import locale

print(f'{"<" * 15} Task_1 {">" * 15}')
"""
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных. 
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных
"""

words = ['разработка', 'сокет', 'декоратор']

for word in words:
    print(f'Type - {type(word)}, content - {word}')

uni_words = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
             '\u0441\u043e\u043a\u0435\u0442',
             '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for u_word in uni_words:
    print(f'Type - {type(word)}, content - {word}')

print(f'{"<" * 15} Task_2 {">" * 15}')
"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных
"""

words = [b'class', b'function', b'method']

for word in words:
    print(f'Type - {type(word)}, content - {word}, length - {len(word)}')

print(f'{"<" * 15} Task_3 {">" * 15}')
"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе
"""

words = ['attribute', 'класс', 'функция', 'type']

for word in words:
    if len(word.encode('ascii', 'ignore')) == 0:
        print(f'Слово {word} невозможно записать в байтовом типе')
"""
Не у верен, что правильно и изящно выполнил данное задание) 
Но мне показалось, что это более интересно, чем просто пытаться каждое слово по отдельности перевести.
"""

print(f'{"<" * 15} Task_4 {">" * 15}')
"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode)
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    print(f'Преобразовываем слово {word}')
    encode_word = word.encode('utf-8')
    print(f'Type - {type(encode_word)}, content - {encode_word}')
    decode_word = encode_word.decode('utf-8')
    print(f'Type - {type(decode_word)}, content - {decode_word}')

print(f'{"<" * 15} Task_5 {">" * 15}')
"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице
"""

args = [['ping', 'google.com'], ['ping', 'yandex.ru']]

for arg in args:
    subprocess_ping = subprocess.Popen(arg, stdout=subprocess.PIPE)

    for line in subprocess_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))


print(f'{"<" * 15} Task_6 {">" * 15}')
"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое
"""

strings = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w+') as f:
    for string in strings:
        f.write(string + '\n')

print(locale.getpreferredencoding())

with open('test_file.txt', encoding='utf-8', errors='replace') as f:
    print(f.read())
