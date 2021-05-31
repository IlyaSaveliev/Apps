import csv
import re
import json
import yaml
import os

print(f'{"<" * 15} Task_1 {">" * 15}')
"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. 
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. 
В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""


def get_data():
    data = []
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    with open('info_1.txt') as f:
        for line in f.readlines():
            data += re.findall(r'^(\w[^:]+).*:\s+([^:\n]+)\s*$', line)

    with open('info_2.txt') as f:
        for line in f.readlines():
            data += re.findall(r'^(\w[^:]+).*:\s+([^:\n]+)\s*$', line)

    with open('info_3.txt') as f:
        for line in f.readlines():
            data += re.findall(r'^(\w[^:]+).*:\s+([^:\n]+)\s*$', line)

    for item in data:
        os_prod_list.append(item[1]) if item[0] == main_data[0][0] else None
        os_name_list.append(item[1]) if item[0] == main_data[0][1] else None
        os_code_list.append(item[1]) if item[0] == main_data[0][2] else None
        os_type_list.append(item[1]) if item[0] == main_data[0][3] else None

    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data

def write_to_cvs(file):
    data = get_data()

    with open('main_info.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        for line in data:
            writer.writerow(line)
    print(data)        

print(write_to_cvs('main_info.csv'))

print(f'{"<" * 15} Task_2 {">" * 15}')
"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date). 
Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""


def write_order_to_json(item, quantity, price, buyer, date):
    orders = []
    data = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}

    if not os.path.isfile('orders.json'):
        orders.append(data)
        with open('orders.json', 'w') as f:
            f.write(json.dumps(orders, indent=4))
        print(f'Был создан файл orders.json и в него были записаны следующие данные: {data}')

    else:
        with open('orders.json') as f:
            new_order = json.load(f)

        new_order.append(data)
        with open('orders.json', 'w') as f:
            f.write(json.dumps(new_order, indent=4))
        print(f'В файл были записаны следующие данные: {data}')


write_order_to_json('books', '2', '800', 'buyer1', '01.01.2021')
write_order_to_json('books2', '2', '800', 'buyer1', '01.01.2021')
write_order_to_json('books3', '2', '800', 'buyer1', '01.01.2021')

print(f'{"<" * 15} Task_3 {">" * 15}')
"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

data = {'goods': ['Motherboards', 'CPU', 'RAM', 'GPU'],
        'goods_quantity': 4,
        'goods_price': {
            'Motherboards': '300€',
            'CPU': '400€',
            'RAM': '200€',
            'GPU': '900€',
        }
        }

with open('file.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

with open('file.yaml') as f:
    print(f.read())
