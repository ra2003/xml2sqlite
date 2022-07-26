#/d:/2021_8_16_oborot/26.08.2021_parse_all_files_in_directory_1.py (git)
'''
Raw_Plan:
1. Parse all directories (unzipped)
    1.1. 
2. Write to sqlite_table

Рабочая идея:
1. Читаю по очереди все файлы xml в каталоге.
2. Обрабатываю их по очереди в csv файлы (кладу в отдельный каталог для csv).
Наименование файлов 1 в 1, только расширение меняется .xml ===>>> .csv
3. Когда все файлы xml обработались в .csv ===>>> обрабатываю всю папку csv ===>>>
write data to sqlite.
'''


import os
import xml.etree.ElementTree as Xet

def parse_dii():
    '''
    !!! перебрать все файлы в директории, открыть, записать нужные данные в sqlite
    '''
    path = 'D:/2021_8_16_oborot/ish_unziped/'
    fileList = os.listdir(path)
    for t in fileList:
        with open('D:/2021_8_16_oborot/ish_unziped/' + t, 'r', encoding='utf-8') as ft:
            base = os.path.splitext(t)[0]
            with open(('D:/2021_8_16_oborot/csv/' + base + '.csv'), 'w+', encoding='utf-8') as f:
            ####!!!!!__error!!!!___with open(('D:/2021_8_16_oborot/csv' + base + '.csv'), 'w+', encoding='utf-8') as f:    
                xmlparse = Xet.parse('D:/2021_8_16_oborot/ish_unziped/' + t)
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
                     
if __name__ == '__main__':
    parse_dii()
