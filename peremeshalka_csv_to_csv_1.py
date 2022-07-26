#/d:/2021_8_16_oborot/26.08.2021_peremeshalka_csv_to_csv_1.py (git)
'''
Raw_Plan:
1. Re csv file from 'D:/2021_8_16_oborot' to 'D:/2021_8_16_oborot/csv
2. Find in file_name "csv..."
'''
import os
import shutil



def parse_dii():
    old_path = 'D:/2021_8_16_oborot'
    new_path = 'D:/2021_8_16_oborot/csv/'
    #old_name = 'csvVO_OTKRDAN5_9965_9965_*.csv'
    #new_name = 'VO_OTKRDAN5_9965_9965_'
    fileList = os.listdir(old_path)
    
    for t in fileList:      
        if t[0:25] == 'csvVO_OTKRDAN5_9965_9965_':
            #print(t[2:])
            t1 = t[3:]
            with open(new_path + t1, 'w+', encoding='utf-8') as f:
                shutil.move(t, new_path+t1) 
                print(new_path + t1)

if __name__ == '__main__':
    parse_dii()
