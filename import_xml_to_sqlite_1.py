#/d:/2021_8_16_oborot/26.08.2021_import_xml_to_sqlite_1.py (git)
'''
26.08.2021 15.14MSK
Чего нет:
1. Записывать спаршенные данные на лету в SQLite.
2. Парсить все файлы в директории, перебирая их по-порядку.

'''
import xml.etree.ElementTree as Xet

f = open('17_your_csv_file.csv', 'w', encoding='utf-8')
xmlparse = Xet.parse('D:/2021_8_16_oborot/ish_unziped/test1.xml')
root = xmlparse.getroot() 

for i in root:
    for i2 in i.findall('СведНП'):
        f.writelines(i2.attrib['НаимОрг'])
        f.write(',')
        f.writelines(i2.attrib['ИННЮЛ'])
        f.write(',')
        for i2 in i.findall('СведДохРасх'):
            f.writelines(i2.attrib['СумДоход'])
            f.write(',')
            f.writelines(i2.attrib['СумРасход'])
            f.write('\n')
f.close()  
