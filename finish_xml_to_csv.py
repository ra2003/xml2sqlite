#D:/2021_8_16_oborot/26.08.2021_finish_xml_to_csv.py

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
        #f.write('\n')
        for i2 in i.findall('СведДохРасх'):
            f.writelines(i2.attrib['СумДоход'])
            f.write(',')
            f.writelines(i2.attrib['СумРасход'])
            f.write('\n')
        
        
f.close()
