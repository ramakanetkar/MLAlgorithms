import sys
from collections import Counter
import math

def get_file_names():
    train_files = open('split.train','r')
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
        c_data = open(c_file,'r')
        for c in c_data:
            c_text.append(c.replace('\n','').lower())
        c_data.close()
    c_Counter.update(c_text)
    #lib dataset
    for l_file in l_files:
        l_data = open(l_file,'r')
        for l in l_data:
            l_text.append(l.replace('\n','').lower())
        l_data.close()
    l_Counter.update(l_text)
    # get vocab, con and lib count
    con_count = len(c_text)
    lib_count = len(l_text)
    vocab_text = set(c_text + l_text)
    vocab_count = len(vocab_text)
    #print('con: ' + str(con_count) + ' ||  lib: ' + str(lib_count) + ' ||  vocab: ' + str(vocab_count))

    lib_top_20 = l_Counter.most_common(20)
    for l in lib_top_20:
        print(l[0], '%.4f' % smoothening(vocab_count, lib_count, int(l[1])))
    print()

    con_top_20 = c_Counter.most_common(20)
    for c in con_top_20:
        print(c[0], '%.4f' % smoothening(vocab_count, con_count, int(c[1])))


if __name__=='__main__':
    main()
