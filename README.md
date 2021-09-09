#/d:/2021_8_16_oborot/README.md (git)
"# xml2sqlite"
##https://habr.com/ru/post/577148/
##All rights reserved Serj Kado aka nasingfaund

##пока не проверенная копия статьи из Хабра

nasingfaund
сегодня, 09.09.2021 в 18:20
# Парсим базу юриков ФНС (велосипедостроение с xml, csv, SQLite и Питоном)
Python*
XML*
SQLite*
Из песочницы

***Замечания: статья для совсем маленьких и крутым спецам по кодингу будет не интересно, лучше ее пропустить. В коде первым комментарием поставлена ссылка на расположение файла с этим кодом для удобства и простоты. Главная задача была получить результат в виде таблицы SQLite. Качество кода оцениваем как ниже среднего, но с заявкой на максимальную простоту. Код написан достаточно просто и без пояснений, но готовы исправиться, поясниться.***

## Вводная
Что хотим сделать: взять данные по юридическим лицам (ЮЛ) РФ за 2019 год (идентификаторы ЮЛ: наименование и ИНН(ЮЛ), оборот, расход) и положить в SQLite.

Для строительства велосипедов **использованы** (но не пострадали):

>Виндовс 7х64

>Питон 3.8.10 (если нет, берем тут).

>В качестве IDE использовалась Visual Studio Code, но абсолютно не принципиально, хоть блокнот.

Подготовительный этап
Открываем командную строку с правами администратора, создаем папку: `(cmd) D:\>mkdir 2021_8_16_oborot` Заходим в созданную папку: `(cmd) D:\>cd 2021_8_16_oborot` и создаем виртуальное окружение для проекта: `(cmd) D:\2021_8_16_oborot>python -m venv venv` при желании можно его активировать в командной строке: `(cmd) D:\2021_8_16_oborot>venv\scripts\activate` Код проекта можно запускать и в командной строке, но нам удобнее использовать для этого IDE и ее терминал. VSCode, как правило, активирует виртуальное окружение самостоятельно, но почему-то не всегда.

## Качаем
Качаем исходный файл. Лучше каким-нибудь даунлодером (например Downloader Master). При попытках качать базы с ФНС и/или Росстата обычным браузером скачка часто обрывается. Исходный файл берем тут. Кладем исходный файл в папку: `D:/2021_8_16_oborot/ish` Там же берем описание структуры набора данных (.xsd).

## Расзиповываем
Посчитали удобнее сразу расзиповать файлы:
```python
# D\2021_8_16_oborot\16.08.2021_unzip_ziped_directory.py

from zipfile import ZipFile

with ZipFile('D:/2021_8_16_oborot/ish/data-20210801-structure-20180801.zip', 'r') as zipObj:
    zipObj.extractall('D:/2021_8_16_oborot/ish_unziped')
```
Запускаем в терминале IDE (правая клавиша мыши и "Run Python file in Terminal"). Если забыли установить пакет zipfile терминал будет ругаться на его отсутствие. Потому устанавливаем нужный пакет в терминале IDE (точно так же и в командной строке Виндоус, но не забываем активировать виртуальное окружение проекта): `(venv) D:\2021_8_16_oborot>pip install zipfile` Предварительно смотрим, что терминал запустился автоматически в виртуальном окружении (по непонятным причинами в VScode обычно запускается виртуальное окружение, но не всегда): `(venv) D:\2021_8_16_oborot>` Если виртуальное окружение не активировалось самостоятельно, то активируем его в ручную, так же как делали в командной строке Виндоус.

**Получили итог: ошибок нет, файл расзиповался в 12 060 xml файлов.**

## Любуемся на xml
Если открыть файлы, то там много лишней (для нашей задачи) информации
```xml
<?xml version="1.0" encoding="UTF-8"?><Файл ИдФайл="VO_OTKRDAN5_9965_9965_20210729_000f7269-b452-4bb0-85ea-3fa614ec3342" ВерсФорм="4.01" ВерсПрог="1.0" ТипИнф="&#x41E;&#x422;&#x41A;&#x420;&#x414;&#x410;&#x41D;&#x41D;&#x42B;&#x415;5" КолДок="92"><ИдОтпр><ФИООтв Фамилия="_" Имя="_"/></ИдОтпр><Документ ИдДок="b6db52b9-1955-4c94-8dd8-cbc4a3da40d8" ДатаДок="30.07.2021" ДатаСост="31.12.2019"><СведНП НаимОрг="&#x41E;&#x411;&#x429;&#x415;&#x421;&#x422;&#x412;&#x41E; &#x421;&#x41E;&#x413;&#x420;&#x410;&#x41D;&#x418;&#x427;&#x415;&#x41D;&#x41D;&#x41E;&#x419;&#x41E;&#x422;&#x412;&#x415;&#x422;&#x421;&#x422;&#x412;&#x415;&#x41D;&#x41D;&#x41E;&#x421;&#x422;&#x42C;&#x42E; &quot;&#x424;&#x418;&#x411;&#x420;&#x41E;&#x422;&#x415;&#x41A;&quot;" ИННЮЛ="7816394401"/><СведДохРасх СумДоход="0.00" СумРасход="0.00"/></Документ><Документ ИдДок="1cd8ab78.....
```
А нам будут нужны только данные по юридическим лицам. В каждом файле xml их от 1 до 100 (примерно):
```
Название юридического лица (само наименование и организационно-правовая форма) находится в исходных файлах в "СведНП НаимОрг",
ИННЮЛ (инн юридического лица) в "СведНП ИННЮЛ",
Доход в "СведДохРасх СумДоход",
Расход в "СведДохРасх СумРасход"
```
Нам показалось удобнее распарсить нужные данные в файлы с такими же названиями, но .csv расширениями. Ну и положить в папку `D:\2021_8_16_oborot\csv` Изначально в тестово-велосипедных целях взяли один файл из 12 060, переименовали его в `test.xml` и написали парсинг и запись данных в `.csv` файл.

```python
# D:\2021_8_16_oborot\26.08.2021_finish_xml_to_csv.py

import xml.etree.ElementTree as Xet

f = open('17_your_csv_file.csv', 'w', encoding='utf-8') # открываем файл для записи результата обработки
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
```
Запустили код, убедились, что все ОК. Данные в каждом из файлов выглядят так:

```csv
ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ФИБРОТЕК",7816394401,0.00,0.00
ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ИЗДАТЕЛЬСКИЙ ДОМ "ТВЕРСКАЯ ЖИЗНЬ",6901026686,0.00,0.00
ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "МРАВ",7726503712,20800000.00,14102000.00
ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "АГРОРЕСУРС",6901026703,470000.00,461000.00
```
Данные по каждому ЮЛ в отдельной строчке, данные разделены запятыми. Теперь можно в цикле брать и парсить все 12 060 файлов.
```python
import os
import xml.etree.ElementTree as Xet

def parse_dii():
   path = 'D:/2021_8_16_oborot/ish_unziped/'
   fileList = os.listdir(path)
   for t in fileList:
      with open('D:/2021_8_16_oborot/ish_unziped/' + t, 'r', encoding='utf-8') as ft:
         base = os.path.splitext(t)[0]
         with open(('D:/2021_8_16_oborot/csv' + base + '.csv'), 'w+', encoding='utf-8') as f:
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
```

## Сами наступаем на грабли, сами правим
После того, как мы записали все csv файлы оказалось, что мы сделали ошибку в путях (пропустили '/' в этой строчке: `with open(('D:/2021_8_16_oborot/csv' + base + '.csv'), 'w+', encoding='utf-8') as f:)` и вместо того, чтобы записать все файлы в директорию `D:\2021_8_16_oborot\csv\` они записались в общую директорию проекта, что не гуд. Пришлось набросать код, чтобы найти все эти файлы и переместить их куда планировали изначально.
```python
# D:\2021_8_16_oborot\26.08.2021_peremeshalka_csv_to_csv_1.py

import os
import shutil

def parse_dii():
   old_path = 'D:/2021_8_16_oborot'
   new_path = 'D:/2021_8_16_oborot/csv/'
   fileList = os.listdir(old_path)
    
   for t in fileList:      
      if t[0:25] == 'csvVO_OTKRDAN5_9965_9965_':
         t1 = t[3:]
         with open(new_path + t1, 'w+', encoding='utf-8') as f:
            shutil.move(t, new_path+t1) 
            print(new_path + t1)

if __name__ == '__main__':
    parse_dii()
```
**Файлы были успешно переименованы и перемещены.**

## Питоним неудачно
Дальше мы написали Питоний код для создания базы данных, таблицы и записи данных в цикле из всех 12060 csv файлов в таблицу. К сожалению сделать этого не удалось, выходили разные ошибки, которые мы не смогли пока решить. С этой проблемой мы разберемся и сразу дополним статью.

## Невзирая ни на что идем дальше
Но так как основная задача была быстро получить финишный результат, то идем дальше к финишу. Поэтому мы пошли так: слили все данные в один csv файл.
```python
# D:\2021_8_16_oborot\05.09.2021_all_csv_to_one_csv.py

import os
import glob

os.chdir("D:/2021_8_16_oborot/csv/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = '\n'.join([open(f, 'r', encoding='utf-8').read().strip() for f in all_filenames ])
with open("combined_csv.csv", 'w') as f:
    f.write(combined_csv)
```    
В процессе работы код использовал почти 0,7ГБ памяти, но благополучно записался.

## Импорт единого csv в SQLite
Раз уж у нас сегодня день велосипедостроения, то для импорта единого файла используем менеджеры SQLite вместо Питона.

В итоге:

>DB browser (SQLite) не смог импортировать этот файл. Вылетел с записью "Это не ошибка, но в записи № 1 125 507 чой-то не то.

>Аналогично не импортнул и SQLite Expert

>Единственный, кто смог импортировать был SQLite Studio (ver.3.3.3). Было записано 1 089 044 строчек в таблицу.

По идее каждая строчка должна быть отдельным данными по одному ЮЛ. Но как выяснилось в таблице нашлось небольшое количество битых строк, у которых в одну ячейку записались данные нескольких ЮЛ, чего, естественно быть не должно. Разбираемся, что это могло быть. Пока предварительная идея, что в исходных данных или в csv файлах есть битые данные, которые ломают правильное формирование таблицы. Но это нужно проверить, найти ошибку.

## В завершение
Планы по исправлению, нахождению причины: продетектить на ошибки (и соответствие схеме) всю исходную директорию, всю директорию с csv файлами, весь "большой" csv файл. Поискать ошибки при записи в таблицу Питоном, вывести ошибки обработки - записи в таблицу.

Замечание. В то же время получить за раз примерно миллион строк с данными по ЮЛ вполне себе неплохо. Если учесть, что максимальное количество действующих ЮЛ доходило по РФ до 4,5 миллиона, а в последнее время было порядка 3 - 3,5 миллиона. То есть у нас есть примерно треть от всех действующих компаний в таблице присутствует. При этом предполагаем, что двойников в таблице нет. Тоже, кстати, надо будет сделать - проверить.

P.S. Код проекта в github пока не положен, в процессе. Будет положен сюда

P.S.2 Изначально, когда мы получили xml-ки, то проверили один из файлов на соответствие схемы. Все было ОК. Но, как мы предполагаем в каких-то из файлов есть ошибки. Когда проверим обновим статью.

А это код проверки только одного (из 12 060) файла на соответствие схемы.
```python
# D:\2021_8_16_oborot\2021_8_16_xsd_validate_xml_file.py

import lxml
from lxml import etree

xml_file = lxml.etree.parse("D:/2021_8_16_oborot/ish_unziped/VO_OTKRDAN5_9965_9965_20210729_000f7269-b452-4bb0-85ea-3fa614ec3342.xml")
xml_validator = lxml.etree.XMLSchema(file="D:/2021_8_16_oborot/structure-20180110.xsd")

is_valid = xml_validator.validate(xml_file)

print(is_valid)
```
P.S.3. Сильно не бейте, это наш первый опус на Хабре.

###### Теги:
#python
#xml
#csv
#sqlite
###### Хабы:
Python
XML
SQLite