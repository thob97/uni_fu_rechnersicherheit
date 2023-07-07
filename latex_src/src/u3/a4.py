#preprocess txt file and open it with pandas
def a():
     #preprocess the file and save it 
     #only if the file doesent already exists
     if not os.path.isfile(p_datafile):
          with open(p_datafile, 'w') as p_file:
               with open(datafile, 'r') as file:
                    for line in file:
                         #add a 'tab' after each passwort frequentcy so it can be used as sep
                         processed_line = re.sub(r'^(\s+)([0-9]+)(\s)',r'\2\t',line)
                         p_file.write(processed_line)

     df = pd.read_csv(p_datafile, sep='\t', header=None,  names=['frequentcys', 'passwords'])
     return df