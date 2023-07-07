import json

#inputfile = 'markov_model_4_6_PIN_rockyou-withcount.txt'
inputfile = 'u4_markov_model.txt'
outputfile = 'p_'+inputfile
top = '\u22A4'

#returns a better dict format of markov_model
#following will be returned:
#eg: '0' : [('5',p1),('2',p2),('9',p3)...]
#    '1' : [('2',p1),('6',p2),('0',p3)...]
# where p1>p2>p3. so the possibilitys are sorted.
#that will allow us to get the 'best' edge if we search for
# an edge for a specific char (eg: result['1'][0][0] will return '2')
def preprocessing(markov_model):
    #edge from v->e
    #note that the edges of list_markov are sorted.
    #eg '00':p, '01':p, '02':p, '03':p
    # where p stands for a possibility 
    list_markov = list(markov_model)
    v = list_markov[0][0]
    temp = []
    result = {}
    for edge in list_markov:
        #if a new different v1 (char) occurs
        #we can save our current temp in the result
        #and start to calc for the new v1(char)
        #because the previous v will not occur again
        #as list_markov edges are sorted
        if v != edge[0]:
            result[v] = sorted(temp, reverse=True)
            v = edge[0]
            temp = []

        #append the possibility and e
        #but only if e != top
        #as our pin has a fixed len, we dont the end symbol
        if edge[1:] != top:
            temp.append( ( markov_model[edge], edge[1:]) )

    #ad the last digit (9) will be skipped otherwise
    result[v] = sorted(temp, reverse=True)
    return result

def guess_password(ordered_markov_model, markov_model ,accuracy, observed_digit, num_of_output_pins):
    result = []
    for i_1 in range(accuracy):
        #add the first (second) char to the pin and calc the probability
        temp_prob_1, temp_char_1 = ordered_markov_model[observed_digit][i_1]
        pin_1 = observed_digit + temp_char_1
        prob_1 = 1 * temp_prob_1

        for i_2 in range(accuracy):
            #add 
            temp_prob_2, temp_char_2 = ordered_markov_model[temp_char_1][i_2]
            pin_2 = pin_1 + temp_char_2
            prob_2 = prob_1 * temp_prob_2

            for i_3 in range(accuracy):
                #add 
                temp_prob_3, temp_char_3 = ordered_markov_model[temp_char_2][i_3]
                pin_3 = pin_2 + temp_char_3
                prob_3 = prob_2 * temp_prob_3

                #last char (digit) of the pin has to be the top symbol top = '\u22A4' 
                #so add that to the pin and calculate the probability of that edge with the normal markov_model
                pin_3 += top
                prob_3 *= markov_model[temp_char_3+top]

                #append result and drop lowest
                result.append( (prob_3, pin_3) )
                drop_lowest(result, num_of_output_pins)

    return result

#searches for the lowest prob in tupel_list and removes it
#but only if there are already to many items in tupel_list
def drop_lowest(tupel_list, num_of_output_pins):
    if len(tupel_list) <= num_of_output_pins:
        return tupel_list
    else:
        min = 1
        elem = (0,0)
        for tupel in tupel_list:
            if tupel[0] < min:
                elem = tupel
                min = tupel[0]
        tupel_list.remove(elem)
        return tupel_list

    
def main():
    #open markov_model file
    markov_model = {}
    with open(inputfile,'r') as file:
        markov_model = json.load(file)

    ordered_markov_model = preprocessing(markov_model)
    
    #write processed_makrov_model to file
    with open(outputfile, "w") as outfile: 
        json.dump(ordered_markov_model, outfile, indent=4)

    result = guess_password(ordered_markov_model, markov_model, 4, '1', 3)

    print(result)

main()