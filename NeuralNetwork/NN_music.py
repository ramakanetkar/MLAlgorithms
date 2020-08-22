import numpy as np
import sys
def main():
    #input_array = preprocessing(get_array1('music_train.csv'))
    input_array = preprocessing(get_array1(sys.argv[1]))
    #output_array = get_array2('music_train_keys.txt')
    output_array = get_array2(sys.argv[2])
    #weights1 = get_array1('music_weights_1.csv',False)
    weights1 = get_array1(sys.argv[4],False)
    #weights2 = get_array2('music_weights_2.csv')
    weights2 = get_array2(sys.argv[5])
    gdw1 = weights1.copy()
    gdw2 = weights2.copy()
    gd(input_array, output_array, gdw1, gdw2)
    print('GRADIENT DESCENT TRAINING COMPLETED!')
    sgdw1 = weights1.copy()
    sgdw2 = weights2.copy()
    for x in range(10000):
        sgd(input_array, output_array, sgdw1, sgdw2, x)
    print('STOCHASTIC GRADIENT DESCENT TRAINING COMPLETED! NOW PREDICTING.')
    #test_array = preprocessing(get_array1('music_dev.csv'))
    test_array = preprocessing(get_array1(sys.argv[3]))
    prediction(test_array,sgdw1,sgdw2)

def prediction(test_array, w1, w2):
    test_shape = list(np.shape(test_array))
    for i in range(int(test_shape[0])):
        input_layer = addbias(test_array[i].reshape(1,4))
        hidden_layer = addbias(sigmoid(np.dot(input_layer, w1)))
        output_layer = sigmoid(np.dot(hidden_layer, w2))
        if output_layer[0,0] > 0.5:
            print('yes')
        else:
            print('no')
    
def gd(input_array, output_array, gdw1, gdw2):
    old_loss, new_loss, loss_diff = 0,0,0
    run_count = 0
    while (loss_diff >=0):
        input_layer = addbias(input_array)
        hidden_layer = addbias(sigmoid(np.dot(input_layer, gdw1)))
        output_layer = sigmoid(np.dot(hidden_layer, gdw2))
        output_error = output_array - output_layer
        error_sq = output_error**2
        output_delta = output_error * output_layer * (1-output_layer)
        hidden_layer_error = output_delta.dot(gdw2.T)
        hidden_layer_delta = removebias(hidden_layer_error * (hidden_layer)* (1- hidden_layer))
        gdw2 += 0.04*np.dot(hidden_layer.T,output_delta)
        gdw1 += 0.04*np.dot(input_layer.T,hidden_layer_delta)
        if run_count == 0:
            old_loss, loss_diff = 0,0
            new_loss = np.sum(error_sq)/2
        else:
            old_loss = new_loss
            new_loss = np.sum(error_sq)/2
            loss_diff = (old_loss-new_loss)
        if loss_diff >= 0:
            print(new_loss)
        run_count += 1

def sgd(input_array, output_array, sgdw1, sgdw2, count):
    input_shape = list(np.shape(input_array))
    sgdloss = 0
    for i in range(int(input_shape[0])):
        input_layer = addbias(input_array[i].reshape(1,4))
        hidden_layer = addbias(sigmoid(np.dot(input_layer, sgdw1)))
        output_layer = sigmoid(np.dot(hidden_layer, sgdw2))
        output_error = output_array[i].reshape(1,1) - output_layer
        error_sq = output_error**2
        output_delta = output_error * output_layer * (1-output_layer)
        hidden_layer_error = output_delta.dot(sgdw2.T)
        hidden_layer_delta = removebias(hidden_layer_error * (hidden_layer)* (1- hidden_layer))
        sgdw2 += 0.4*np.dot(hidden_layer.T,output_delta)
        sgdw1 += 0.4*np.dot(input_layer.T,hidden_layer_delta)
        sgdloss += np.sum(error_sq)/2
    if count <15:
        print(sgdloss)
            
        
def preprocessing(array):
    minimum = array.min(axis=0)
    maximum =array.max(axis=0)
    minimum[0] = 1900
    maximum[0] = 2000
    minimum[1] = 0
    maximum[1] = 7
    array = (array - minimum)/(maximum- minimum)
    return array

def addbias(array):
    x,y = np.shape(array)
    x0 = np.ones((x,1))
    bias_array = np.concatenate((x0,array), axis=1)
    return bias_array

def removebias(array):
    return np.delete(array,0,axis=1)

def get_array1(fileName, header=True):
        #input File
    input_file = open(fileName,'r')
    if header == True:
        headers = input_file.readline().rstrip().split(',')
    input_list = []
    for i in input_file:
        line = i.rstrip().split(',')
        for j in range(len(line)):
            if line[j] == 'yes' or line[j] == 'Yes':
                line[j] = 1
            elif line[j] == 'no' or line[j] == 'No':
                line[j] = 0
            else:
                line[j] = float(line[j])
        input_list.append(line)
    input_array = np.array(input_list)
    return input_array

def get_array2(fileName):
    output_file = open(fileName,'r')
    output_list = []
    for o in output_file:
        o_line = o.rstrip()
        if o_line == 'yes' or o_line == 'Yes':
            o_line = 1
        elif o_line == 'no' or o_line == 'No':
            o_line = 0
        output_list.append(float(o_line))
    output_array = np.array(output_list).reshape(len(output_list),1)
    return output_array

def sigmoid(x):
    return 1/(1+ np.exp(-x))

if __name__=="__main__":
    main()
