import sys
from collections import Counter
import math
import pandas as pd
def get_file_names():
    train_files = open('split.train1','r')
    train_files_list = []
    for t in train_files:
        train_files_list.append(t.replace('\n',''))
    con_train_list = [ name for name in train_files_list if name[0].lower() == 'c']
    lib_train_list = [ name for name in train_files_list if name[0].lower() == 'l']
    train_files.close()
    return con_train_list,lib_train_list


def word_probability(counter, count, vocab):
    wordCount_list = list(counter.items())
    word_probability = {}
##    i = 0
    for word in wordCount_list:
        w = word[0]
        w_count = float(word[1])
        word_probability[w] = (w_count+1)/(count + vocab)
##        if i <10:
##            print(word_probability)
##        i +=1
    return word_probability

def test_nb(word_list, word_probabilities):
    #print('calculating log')
    log_value = 0
    key = [ key for key, value in word_probabilities.items()]
    for i in range(len(word_list)):
        #print(word_list[i])
        if word_list[i] in key:
            #print(word_probabilities[word_list[i]])
            log_value += math.log(word_probabilities[word_list[i]])
            #print(log_value)
    return log_value

def get_accuracy(actual_list, predicted_list):
    true_value = 0
    false_value = 0
    for i in range(len(actual_list)):
        if actual_list[i] == predicted_list[i]:
            true_value +=1
        else:
            false_value +=1
    return true_value / (true_value + false_value)
            
    
def main():
    c_list, l_list = get_file_names()
    c_tgt_prob = math.log(len(c_list)/(len(c_list) + len(l_list)))
    l_tgt_prob = math.log(len(l_list)/(len(c_list) + len(l_list)))
    print(len(c_list))
    print(len(l_list))
    print(c_tgt_prob)
    print(l_tgt_prob)
    c_Counter = Counter()
    l_Counter = Counter()
    c_text = []
    l_text = []
    for file in c_list:
        c_file = open(file,'r')
        for c in c_file:
            c_value = c.replace('\n','').lower()
            c_text.append(c_value)
            c_Counter[c_value] +=1
        c_file.close()
        
    print('C-Counter')
    con_DF = pd.DataFrame(list(c_Counter.items()))
    con_DF.to_csv('Con_Counter.csv',sep=',',encoding='utf-8')
    
    for file in l_list:
        l_file = open(file,'r')
        for l in l_file:
            l_value = l.replace('\n','').lower()
            l_text.append(l_value)
            l_Counter[l_value] +=1
    con_n = len(list(set(c_text)))
    
    print('L-Counter')
    lib_DF = pd.DataFrame(list(l_Counter.items()))
    lib_DF.to_csv('Lib_Counter.csv',sep=',',encoding='utf-8')
    
    print(con_n)
    lib_n = len(list(set(l_text)))
    print(lib_n)
    vocab = len(list(set(c_text + l_text)))
    print(vocab)
    con_probabilities = word_probability(c_Counter,con_n,vocab)
    
    con_prob_DF = pd.DataFrame(list(con_probabilities))
    con_prob_DF.to_csv('Con_Prob.csv',sep=',',encoding='utf-8')
    
    lib_probabilities = word_probability(l_Counter,lib_n,vocab)
    
    lib_prob_DF = pd.DataFrame(list(lib_probabilities))
    lib_prob_DF.to_csv('lib_Prob.csv',sep=',',encoding='utf-8')

    
    test_file_names = open('split.test1','r')
    actual_value = []
    predicted_value = []
    for t in test_file_names:
        test_words = []
        c_prob ,l_prob, c_final_prob , l_final_prob = 0,0,0,0
        test_file_name = t.replace('\n','')
        actual_value.append(test_file_name[0].upper())
        words = open(test_file_name,'r')
        for word in words:
            test_words.append(word.replace('\n','').lower())
        words.close()
        print('test words')
        test_DF = pd.DataFrame(test_words)
        test_DF.to_csv('test.csv',sep=',',encoding='utf-8')
        c_prob = test_nb(test_words,con_probabilities) # write this function
        l_prob = test_nb(test_words,lib_probabilities)
        c_final_prob = c_tgt_prob + c_prob
        l_final_prob = l_tgt_prob + l_prob
        print(c_final_prob)
        print(l_final_prob)
##        if c_final_prob >= l_final_prob:
##            predicted_value.append('C')
##            print('C')
##        else:
##            predicted_value.append('L')
##            print('L')
##    accuracy = get_accuracy(actual_value,predicted_value)
##    print('Accuracy: ' + str(accuracy))
    


if __name__=='__main__':
    main()
