import os
import time
import pandas as pd
import re
import linecache
import math, numpy

datafile = 'rockyou-withcount.txt'
p_datafile = 'p_rockyou-withcount.txt'
top_10_passwords = '10_most_frequent.txt'
error_file = 'errors.txt'
p1_file = 'p1.csv'
task_j_file = 'task_j_file.csv'
stats_file = 'stats_file.txt'

#preprocess txt file and open it with pandas
def a():
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
def b(df):
     #find all NaN/ error rows
     nan_rows = df[df['passwords'].isna()]
     #save the index of error rows to list
     list_nan_index = nan_rows.index.tolist()
     #write error rows to a new file
     with open(error_file, 'w') as e_file:
          for index in list_nan_index:
               #find line in file
               line = linecache.getline(p_datafile, index+1)
               format_line = str(index) + ':' + line
               e_file.write(format_line)

     #correct errors in df (drop the rows)
     df = df.drop(df.index[list_nan_index])
     #reset index
     df.reset_index(inplace=True, drop=True)

     #start writing stats
     with open(stats_file, 'w') as file:
          file.write(df.describe().to_string() + '\n')
          file.write('median:\t' + str(df['frequentcys'].median()) + '\n')
          file.write('mode:\t' + str(df['frequentcys'].mode()) + '\n' )
          file.write('var:\t' + str(df.var()) + '\n' ) 
     return df

#writes the ten most frequent passwords to a file
def c(df):
     with open(top_10_passwords, 'w') as file:
          df.head(10).to_string(file)

#create passwordset P1
def d_e(df):
     #\A from beginning of the string till \z end: looks for a word with 7-32 chars
     a = '\A(?=\w{7,32}\Z)'
     # [^a-z]* not A-Z 0-many times and then one time A-Z: looks for at least one upper case char
     b = '(?=[^A-Z]*[A-Z])'
     # D* no digits for 0-many times and then one digit: looks for at least one digit
     c = '(?=\D*\d)'
     p1 = df.loc[df['passwords'].str.contains(a+b+c, regex=True)].copy()
     #reset index
     p1.reset_index(inplace=True, drop=True)
     return p1

#calculate the probability of each password in p1
def f(p1, sum_of_frequentcys):
     p1['probability'] = p1['frequentcys'] / sum_of_frequentcys 
     return p1

#calculate Shannon Entropy of p1
def g(p1, sum_of_frequentcys):
     shannon_entropy = (p1['probability'] * numpy.log2(p1['probability'])*-1).sum() 
     return shannon_entropy

#calculates expected num of guesses to crack k accounts
def h(p1, num_of_accounts_to_crack): 
     #sort values by probability from high to low (i > i+1)
     p1.sort_values(by=['probability'], ascending = False, inplace = True)
     #reset index
     p1.reset_index(inplace=True, drop=True)
     #calc guesswork
     guesswork = (p1['probability']* (p1.index +1 )).sum()
     return num_of_accounts_to_crack*guesswork

#assume sorted###################################################################
def beta_succ(beta,p1):
     return p1['probability'][0:beta].sum()

#this is slooow
def i2(p1,l,k):
    alpha = l/k
    a_work = min([beta for beta in list(range(len(p1))) if beta_succ(beta,p1)>=alpha  ])
    except_fail = (1-beta_succ(a_work,p1))*a_work
    except_succ = (p1['probability'][0:a_work]*list(range(1,a_work+1))).sum()
    return except_fail+except_succ
################################################################################

#calculates expected num of guesses to crack l accounts of k existing accounts
def i(p1):
     l_div_k = 50/200
     sum = 0
     beta = 0
     while sum < l_div_k:
          sum += p1['probability'][beta]
          beta += 1
     return beta

def j(df):
     #get dataframe with password policy
     policy = '\A(?=\w{8,64}\Z)' + '(?=(?:[^A-Z]*[A-Z]){2})' + '(?=[^a-z]*[a-z])' + '(?=(?:\D*\d){2})'
     p_df = df.loc[df['passwords'].str.contains(policy, regex=True)].copy()
     #reset index
     p_df.reset_index(inplace=True, drop=True)

     #calculate the probability of each password 
     sum_of_frequentcys = p_df.iloc[:,0].sum()
     p_df = f(p_df, sum_of_frequentcys)

     #calculate Shannon Entropy of p1
     shannon_entropy = g(p_df, sum_of_frequentcys)

     #calculates number of guesses to crack k accounts
     num_of_guesses = h(p_df, 200)
     #calculates expected num of guesses to crack l accounts of k existing accounts
     num_of_guesses_2 = i(p_df)

     return p_df, shannon_entropy, num_of_guesses, num_of_guesses_2

#write dataframe to file
def write_to_file(df, filename):
     df.to_csv(path_or_buf=filename, sep='\t')


def main():
     #open txt file with pandas
     df = a()

     #find and correct errors
     df = b(df)

     #write top 10 passwords to file
     c(df)

     #create passwordset P1
     p1 = d_e(df)

     #calculate the probability of each password in p1
     sum_of_frequentcys = p1.iloc[:,0].sum()
     p1 = f(p1, sum_of_frequentcys)

     #calculate Shannon Entropy of p1
     shannon_entropy = g(p1, sum_of_frequentcys)

     #calculates number of guesses to crack k accounts
     num_of_guesses = h(p1, 200)

     #calculates expected num of guesses to crack l accounts of k existing accounts
     num_of_guesses_2 = i(p1)

     #write p1 to file
     write_to_file(p1, p1_file)

     #calculates tasks f-i for j
     p_df, j_shannon_entroyp, j_num_of_guesses, j_num_of_guesses_2 = j(df)

     #write onw_policy_dataframe to file
     write_to_file(p_df, task_j_file)
     
     print('Results for p1')
     print('password sample size: ',p1['frequentcys'].sum() ,' shannon_entropy: ',shannon_entropy, ' guesses to crack 200 accounts: ',num_of_guesses, ' guesses to crack 50 of 200 accounts: ', num_of_guesses_2)
     print()
     print('Results for own password policy')
     print('password sample size: ',p_df['frequentcys'].sum() ,' shannon_entropy: ',j_shannon_entroyp, ' guesses to crack 200 accounts: ',j_num_of_guesses, ' guesses to crack 50 of 200 accounts: ', j_num_of_guesses_2)

if __name__ == "__main__":
     start_time = time.time()
     main()
     #print execution time
     print("--- %s seconds ---" % (time.time() - start_time))
