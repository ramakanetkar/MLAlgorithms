import sys
from collections import Counter
import math
import time
start = time.time()
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
    true_value = 0
    false_value = 0
    for i in range(len(actual_list)):
        if actual_list[i] == predicted_list[i]:
            true_value +=1
        else:
            false_value +=1
    return true_value / (true_value + false_value)


def main():
    #get file names in the train dataset
    c_files, l_files, c_file_count, l_file_count = get_file_names()
##    print(c_files)
##    print(l_files)
    #Calculate prior for con and lib target values
    c_prior = math.log(c_file_count/(c_file_count + l_file_count))
    l_prior = math.log(l_file_count/(c_file_count + l_file_count))
    #print(c_prior)
    #print(l_prior)
    # Count and list words in con and lib dataset separately
    c_Counter = Counter()
    l_Counter = Counter()
    c_text = []
    l_text = []
    #con dataset
    for c_file in c_files:
        c_data = open(c_file,'r')
        for c in c_data:
            c_value = c.replace('\n','').lower()
            c_text.append(c_value)
            c_Counter[c_value] +=1
##        print(len(c_text))
        c_data.close()
    #lib dataset
    for l_file in l_files:
        l_data = open(l_file,'r')
        for l in l_data:
            l_value = l.replace('\n','').lower()
            l_text.append(l_value)
            l_Counter[l_value] +=1
##        print(len(l_text))
        l_data.close()
    # get vocab, con and lib count
    vocab_text = list(set(c_text + l_text))
    con_count = len(list(set(c_text)))
    lib_count = len(list(set(l_text)))
    vocab_count = len(vocab_text)
    #print('con: ' + str(con_count) + ' ||  lib: ' + str(lib_count) + ' ||  vocab: ' + str(vocab_count))

    #convert counter into list of words and list of word count for con
    con_training_words = []
    con_word_count = []
    for word, count in c_Counter.items():
        con_training_words.append(word)
        con_word_count.append(count)
    #print(len(con_training_words))
    #print(len(con_word_count))
    #convert counter into list of words and list of word count for lib
    lib_training_words = []
    lib_word_count = []
    for word, count in l_Counter.items():
        lib_training_words.append(word)
        lib_word_count.append(count)
    #print(len(lib_training_words))
    #print(len(lib_word_count))

    #get file names from test dataset
    test_files = open('split.test','r')
    actual_values = []
    predicted_values = []
    for test_file in test_files:
        t_file = test_file.replace('\n','')
        test_data = open(t_file,'r')
        test_words = []
        #get words in each file
        for t in test_data:
            t_value = t.replace('\n','').lower()
            test_words.append(t_value)
        #calculate log product for words in test_words
        for t_word in test_words:
            if t_word in vocab_text:
                #con log product
                con_index = None
                t_con_word_count = 0
                con_log_product = 0
                if t_word in con_training_words:
                    con_index = con_training_words.index(t_word)
                    t_con_word_count = con_word_count[con_index]
                    con_log_product += smoothening(vocab_count,con_count,t_con_word_count)
                else:
                    con_log_product += smoothening(vocab_count,con_count,0)
                #lib log product
                lib_index = None
                t_lib_word_count = 0
                lib_log_product = 0
                if t_word in lib_training_words:
                    lib_index = lib_training_words.index(t_word)
                    t_lib_word_count = lib_word_count[lib_index]
                    lib_log_product += smoothening(vocab_count,lib_count,t_lib_word_count)
                else:
                    lib_log_product += smoothening(vocab_count,lib_count,0)
        con_log = c_prior + con_log_product
        lib_log = l_prior + lib_log_product
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
    print(get_accuracy(actual_values,predicted_values))
      

if __name__=='__main__':
    main()

end =time.time()
print(end-start)
