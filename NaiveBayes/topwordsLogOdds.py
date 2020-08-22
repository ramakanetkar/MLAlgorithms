import sys
from collections import Counter
import math

def get_file_names():
    train_files = open(sys.argv[1],'r',encoding="latin-1")
    train_files_list = []
    for t in train_files:
        train_files_list.append(t.replace('\n',''))
    con_train_list = [ name for name in train_files_list if name[0].lower() == 'c']
    lib_train_list = [ name for name in train_files_list if name[0].lower() == 'l']
    train_files.close()
    return con_train_list,lib_train_list, len(con_train_list), len(lib_train_list)

def smoothening(vocab, n, nk):
    numerator = float(nk+1)
    denominator = float(n+vocab)
    return_value = (numerator/denominator)
    return return_value

def get_log(p1,p2):
    result = math.log(p1/p2)
    return result

def main():
    #get file names in the train dataset
    c_files, l_files, c_file_count, l_file_count = get_file_names()
    # Count and list words in con and lib dataset separately
    c_Counter = Counter()
    l_Counter = Counter()
    c_text = []
    l_text = []
    #con dataset
    for c_file in c_files:
        c_data = open(c_file,'r',encoding="latin-1")
        for c in c_data:
            c_text.append(c.replace('\n','').lower())
        c_data.close()
    c_Counter.update(c_text)
    #lib dataset
    for l_file in l_files:
        l_data = open(l_file,'r',encoding="latin-1")
        for l in l_data:
            l_text.append(l.replace('\n','').lower())
        l_data.close()
    l_Counter.update(l_text)
    # get vocab, con and lib count
    con_count = len(c_text)
    lib_count = len(l_text)
    vocab_text = set(c_text + l_text)
    con_text = set(c_text) # for faster search
    lib_text = set(l_text) # for faster search
    vocab_count = len(vocab_text)
    #print('con: ' + str(con_count) + ' ||  lib: ' + str(lib_count) + ' ||  vocab: ' + str(vocab_count))
    #con_word_Probability_dict
    con_words_prob = {}
    for word, count in c_Counter.items():
        con_words_prob[word] = smoothening(vocab=vocab_count, n=con_count, nk = count)
    con_freq0_prob = smoothening(vocab=vocab_count, n=con_count, nk = 0)

    #lib_word_Probability_dict
    lib_words_prob = {}
    for word, count in l_Counter.items():
        lib_words_prob[word] = smoothening(vocab=vocab_count, n=lib_count, nk = count)

    lib_freq0_prob = smoothening(vocab=vocab_count, n=lib_count, nk = 0)

    con_log_odds = {}
    lib_log_odds = {}
    for v in vocab_text:
        if v in con_text and v in lib_text:
            con_log_odds[v] = get_log(con_words_prob[v],lib_words_prob[v])
            lib_log_odds[v] = get_log(lib_words_prob[v],con_words_prob[v])
        elif v in con_text and v not in lib_text:
            con_log_odds[v] = get_log(con_words_prob[v],lib_freq0_prob)
            lib_log_odds[v] = get_log(lib_freq0_prob,con_words_prob[v])
        elif v not in con_text and v in lib_text:
            con_log_odds[v] = get_log(con_freq0_prob,lib_words_prob[v])
            lib_log_odds[v] = get_log(lib_words_prob[v],con_freq0_prob)
            

    sorted_lib_log_odds = sorted(lib_log_odds.items(), key = lambda kv: kv[1], reverse=True)

    print_count1 = 0
    for sorted_values in sorted_lib_log_odds:
        if print_count1 >19:
            break
        print( sorted_values[0],'%0.4f' % sorted_values[1])
        print_count1 +=1
    print()

    sorted_con_log_odds = sorted(con_log_odds.items(), key = lambda kv: kv[1], reverse=True)

    print_count = 0
    for sorted_values in sorted_con_log_odds:
        if print_count >19:
            break
        print( sorted_values[0],'%0.4f' % sorted_values[1])
        print_count +=1

if __name__=='__main__':
    main()
