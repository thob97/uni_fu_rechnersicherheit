import time
import pandas as pd
import json

datafile = '4_6_PIN_rockyou-withcount.txt'
outputfile = 'markov_model_'+datafile
top = '\u22A4'
bot = '\u22A5'

def init_database():
     #read datafile
     df = pd.read_csv(datafile, sep='\t', index_col = 0, dtype={'passwords': str})
     #add top and bottom
     df['passwords'] = bot + df['passwords'] + top
     return df

#count occurrences of chars in the password dataset
def count_occurrences(df, alphabet):
     occurrences = {}
     #for every char in alphabet (digit)
     for char in alphabet:
          #count the occurrence of that char, for every password in the database (* by frequentcys)
          df['occurrences'] = count_char(df['passwords'] , char) * df['frequentcys']
          #save result to dict
          occurrences[char] = df['occurrences'].sum()
     return occurrences

#count occurrence of a char in a string
def count_char(list, char):
     result = []
     for string in list:
          result.append(string.count(char))
     return result

#returns an alphabet for a makrov model +1
#returns an alphabet with every possible combination of the 2 input alphabets 
# if you combine the chars in them
#the if clause will prevent that we get edges which will never occur
#e.g. T0, T1, ... TBot, ... 0Bot, 1Bot...
def markov_alphabet(alp1, alp2):
     return [char1+char2 for char1 in alp1 for char2 in alp2 if char1 != top and char2 != bot]

#creates a makrov model / calcs the probability of the edge_set
def create_makrov_model(occ, alphabet, occ_edge_set):
     markov_model = {}
     for char in alphabet:
          #divides the total num of edges by the total number of the beginning vertice
          #e.g. occ_edge_set['01'] = 10 / occ['0'] = 20  => 0.5
          markov_model[char] = occ_edge_set[char] / occ[char[0]]
     return markov_model


def main():
     df = init_database()
     print(df)

     print()
     alphabet_1 = [bot,'0','1','2','3','4','5','6','7','8','9',top]
     occ = count_occurrences(df, alphabet_1)
     print('occ: ', occ)

     print()
     print('alphabet_1: ', alphabet_1)

     print()
     alphabet_2 = markov_alphabet(alphabet_1, alphabet_1)
     print('alphabet_2: ', alphabet_2)

     print()
     occ_edge_set = count_occurrences(df, alphabet_2)
     print('occ_edge_set: ', occ_edge_set)

     print()
     markov_model = create_makrov_model(occ, alphabet_2, occ_edge_set)
     print('markov_model: ', markov_model)

     with open(outputfile, "w") as outfile: 
          json.dump(markov_model, outfile, indent=4)

main()