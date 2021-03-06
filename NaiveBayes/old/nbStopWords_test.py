import sys
from collections import Counter
import math
#import time
#start = time.time()
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
    return_value = math.log(numerator/denominator)
    return return_value

def get_accuracy(actual_list, predicted_list):
    total_count = len(actual_list)
    true_predicted = sum([1.0 if actual_list[i] == predicted_list[i] else 0.0 for i in range(total_count)])
    return true_predicted / total_count

def main():
    #get file names in the train dataset
    c_files, l_files, c_file_count, l_file_count = get_file_names()
    #Calculate prior for con and lib target values
    c_prior = math.log(c_file_count/(c_file_count + l_file_count))
    l_prior = math.log(l_file_count/(c_file_count + l_file_count))
    #Frequent count
    frequent_count = 10
    # Count and list words in con and lib dataset separately
    c_Counter = Counter()
    l_Counter = Counter()
    v_Counter = Counter()
    initial_c_text = []
    initial_l_text = []
    #con dataset
    for c_file in c_files:
        c_data = open(c_file,'r')
        for c in c_data:
            initial_c_text.append(c.replace('\n','').lower())
        c_data.close()
    
    #lib dataset
    for l_file in l_files:
        l_data = open(l_file,'r')
        for l in l_data:
            initial_l_text.append(l.replace('\n','').lower())
        l_data.close()
    # removing frequent words
    v_Counter.update(initial_c_text + initial_l_text)
    remove_list = [v[0] for v in v_Counter.most_common(frequent_count)]
    #print(remove_list)
    c_text = [ c for c in initial_c_text if c not in remove_list]
    l_text = [l for l in initial_l_text if l not in remove_list]
    c_Counter.update(c_text)
    l_Counter.update(l_text)
    # get vocab, con and lib count
    #convert counter into list of words and list of word count for con
    con_count = len(c_text)
    con_training_words = []
    con_word_count = []
    for word, count in c_Counter.items():
        con_training_words.append(word)
        con_word_count.append(count)
    #print(len(con_training_words))
    #print(len(con_word_count))
    #convert counter into list of words and list of word count for lib
    lib_count = sum(l_Counter.values())
    lib_training_words = []
    lib_word_count = []
    for word, count in l_Counter.items():
        lib_training_words.append(word)
        lib_word_count.append(count)
    #print(len(lib_training_words))
    #print(len(lib_word_count))
    set_con_training_words = set(con_training_words)
    set_lib_training_words = set(lib_training_words)
    vocab_text = set(con_training_words + lib_training_words)
    vocab_count = len(vocab_text)
    #print('con: ' + str(con_count) + ' ||  lib: ' + str(lib_count) + ' ||  vocab: ' + str(vocab_count))

    #get file names from test dataset
    test_files = open('split.test','r')
    actual_values = []
    predicted_values = []
    for test_file in test_files:
        t_file = test_file.replace('\n','')
        test_data = open(t_file,'r')
        test_words = [t.replace('\n','').lower() for t in test_data]
        #calculate log product for words in test_words
        con_log_product = 0
        lib_log_product = 0
        for t_word in test_words:
            #print(t_word)
            if t_word in vocab_text:
                #con log product
                con_index = None
                t_con_word_count = 0
                if t_word in set_con_training_words:
                    con_index = con_training_words.index(t_word)
                    t_con_word_count = con_word_count[con_index]
                con_log_product += smoothening(vocab_count,con_count,t_con_word_count)
             #   print(con_log_product)
                #lib log product
                lib_index = None
                t_lib_word_count = 0
                if t_word in set_lib_training_words:
                    lib_index = lib_training_words.index(t_word)
                    t_lib_word_count = lib_word_count[lib_index]
                lib_log_product += smoothening(vocab_count,lib_count,t_lib_word_count)
              #  print(lib_log_product)
        con_log = c_prior + con_log_product
        lib_log = l_prior + lib_log_product
        #print(con_log)
        #print(lib_log)
        test_data.close()
        #predict values
        actual_values.append(test_file[0].upper())
        if con_log > lib_log:
            predicted_values.append('C')
            print('C')
        else:
            predicted_values.append("L")
            print("L")
    test_files.close()
    print ('Accuracy:', '%.4f' % get_accuracy(actual_values,predicted_values))
      

if __name__=='__main__':
    main()
#end = time.time()
#print(end-start)
