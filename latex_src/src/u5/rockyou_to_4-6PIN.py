import os
import time
import pandas as pd
import re
import linecache
import math, numpy

datafile = 'rockyou-withcount.txt'
p_datafile = 'p_rockyou-withcount.txt'
error_file = 'errors.txt'
output_file = '4_6_PIN.txt'


#preprocess txt file and open it with pandas
def preprocess():
     #preprocess the file and save it 
     #only if the file doesent already exists
     if not os.path.isfile(p_datafile):
          with open(p_datafile, 'w') as p_file:
               with open(datafile, 'r', encoding = "ISO-8859-1") as file:
                    for line in file:
                         #add a 'tab' after each passwort frequentcy so it can be used as sep
                         processed_line = re.sub(r'^(\s+)([0-9]+)(\s)',r'\2\t',line)
                         p_file.write(processed_line)

     df = pd.read_csv(p_datafile, sep='\t', header=None,  names=['frequentcys', 'passwords'])
     return df

#find, write and correct errors and write some usefull data to file
def correct_errors(df):
     #find all NaN/ error rows
     nan_rows = df[df['passwords'].isna()]
     #save the index of error rows to list
     list_nan_index = nan_rows.index.tolist()
     #write error rows to a new file
     #with open(error_file, 'w') as e_file:
     #     for index in list_nan_index:
     #          #find line in file
     #          line = linecache.getline(p_datafile, index+1)
     #          format_line = str(index) + ':' + line
     #          e_file.write(format_line)

     #correct errors in df (drop the rows)
     df = df.drop(df.index[list_nan_index])
     #reset index
     df.reset_index(inplace=True, drop=True)

     return df

#create passwordset P1
def filter_4digits_6digits(df):
     #\A from beginning of the string till \z end: looks for digits with 4-4 chars or 6-6 chars
     a = '(?:\A(?=\d{4,4}\Z)|\A(?=\d{6,6}\Z))'
     df = df.loc[df['passwords'].str.contains(a, regex=True)].copy()
     #reset index
     df.reset_index(inplace=True, drop=True)
     return df

#write dataframe to file
def write_to_file(df, filename):
     df.to_csv(path_or_buf=filename, sep='\t')

def main():
    df = preprocess()
    df = correct_errors(df)
    df = filter_4digits_6digits(df)
    write_to_file(df, output_file)

if __name__ == "__main__":
     start_time = time.time()
     main()
     #print execution time
     print("--- %s seconds ---" % (time.time() - start_time))
