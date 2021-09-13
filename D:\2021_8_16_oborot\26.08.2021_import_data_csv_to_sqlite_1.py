#/d:/2021_8_16_oborot/26.08.2021_import_data_csv_to_sqlite_1.py (git)
'''
!!!
Raw_Plan:
1. Iteration all .csv files in .../csv directory
2. Create work data_base, work_table.
3. import all data in files to sqlite data base
!!!
'''
import sqlite3
import csv
import os

def create_db_table():
    '''
    create database if not exist!!!!
    create table if not exist!!!!
    '''
    conn = sqlite3.connect('D:/2021_8_16_oborot/UL.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS oborot_2019_fns 
             (name_UL text, inn_UL int, oborot_2019 real, rashod_2019 real)''')

    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()


    # Select from the temperature table
    '''query_Table = "SELECT * FROM oborot_2019_fns"
    query_Results = cursor_Object.execute(query_Table)'''

    # Print the Temperature records
    '''for result in query_Results:
        print(result)

    connection_Object.close()'''

def import_csv_to_sqlite():

    con = sqlite3.connect('D:/2021_8_16_oborot/UL.db')
    cur = con.cursor()

   
    path_D = 'D:/2021_8_16_oborot/csv'
    file_List = os.listdir(path_D)
    for x in file_List:
        with open('D:/2021_8_16_oborot/csv/'+x, 'r', encoding='utf-8') as f_in:
            rows = csv.reader(f_in)
            #for row in rows:
                #print(row)
            
            #print(rows, dir(rows), type(rows))
            cur.executemany('INSERT INTO oborot_2019_fns VALUES (?, ?, ?, ?)', rows)
                #cur.executemany('INSERT INTO oborot_2019_fns VALUES (?, ?, ?, ?)', (name_UL, inn_UL, oborot_2019, rashod_2019))

            '''except IOError as e:
                if e.args == 2: # No such file or directory
                    blank_db = sqlite3.connect('D:/2021_8_16_oborot/UL.db')
                    print ('Blank database created')
                else: # permission denied or something else?
                    print (e)'''

            #cur.execute("SELECT * FROM oborot_2019_fns")
            #print(cur.fetchall())

    con.commit()
    con.close()                  

if __name__ == '__main__':
    create_db_table()
    import_csv_to_sqlite()
