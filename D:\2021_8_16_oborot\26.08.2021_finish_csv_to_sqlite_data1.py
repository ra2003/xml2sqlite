#/d:/2021_8_16_oborot/26.08.2021_finish_csv_to_sqlite_data1.py (git)

import sqlite3
import csv

'''def create_table_if_not_exist()'''


conn = sqlite3.connect('D:/2021_8_16_oborot/test.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS data1 
             (name_UL text, inn_UL int, oborot_2019 real, rashod_2019 real)''')

#commit the changes to db			
conn.commit()
#close the connection
conn.close()


# Select from the temperature table
'''query_Table = "SELECT * FROM data1"
query_Results = cursor_Object.execute(query_Table)'''

# Print the Temperature records
'''for result in query_Results:
    print(result)

connection_Object.close()'''


con = sqlite3.connect('D:/2021_8_16_oborot/test.db')
cur = con.cursor()

a_file = open('D:/2021_8_16_oborot/17_your_csv_file.csv', 'r', encoding='utf-8')
rows = csv.reader(a_file)
#cur.executemany("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", rows)
#cur.executemany("INSERT INTO data VALUES (?, ?, ?, ?)", (name_UL, inn_UL, oborot, rashod))
cur.executemany("INSERT INTO data1 VALUES (?, ?, ?, ?)", rows)

cur.execute("SELECT * FROM data1")
print(cur.fetchall())

con.commit()
con.close()
