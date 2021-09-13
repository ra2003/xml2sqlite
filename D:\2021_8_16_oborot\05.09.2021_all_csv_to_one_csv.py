# D:\2021_8_16_oborot\05.09.2021_all_csv_to_one_csv.py

import os
import glob

os.chdir("D:/2021_8_16_oborot/csv/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = '\n'.join([open(f, 'r', encoding='utf-8').read().strip() for f in all_filenames ])
with open("combined_csv_2.csv", 'w') as f:
    f.write(combined_csv)
