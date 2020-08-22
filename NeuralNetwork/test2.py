import numpy as np
def main():
    #neural network
    #output file
    input_array = preprocessing(get_array1('music_train.csv'))
    output_array = get_array2('music_train_keys.txt')
    weights1 = get_array1('music_weights_1.csv',False)
    #print(weights1)
    weights2 = get_array2('music_weights_2.csv')
    for i in range(100):
        gd(input_array[i].reshape(1,4), output_array[i].reshape(1,1), weights1, weights2)

def gd(input_array, output_array, weights1, weights2, descent='gd',print_error = 0):
    
    for i in range(1):
        input_layer = addbias(input_array)
        hidden_layer = addbias(sigmoid(np.dot(input_layer, weights1)))
        #print(hidden_layer)
        output_layer = sigmoid(np.dot(hidden_layer, weights2))
        #print(output_layer)
        output_error = output_array - output_layer
        #print(output_error)
        oe1 = output_error**2 
        #print(np.mean(output_error))
        #print(np.shape(output_error))
        #if i % 10000 == 0 :
        #print(np.sum(oe1)/2)
        print_error += np.sum(oe1)/2
        print(print_error)
        output_delta = output_error * output_layer * (1-output_layer)
        #print(output_delta)
        hidden_layer_error = output_delta.dot(weights2.T)
##        print((hidden_layer_error))
        hidden_layer_delta = removebias(hidden_layer_error * (hidden_layer)* (1- hidden_layer))
        #print(np.shape(input_layer))
        #print(np.shape(hidden_layer_delta))
        weights2 += 0.4*np.dot(hidden_layer.T,output_delta)
        weights1 += 0.4*np.dot(input_layer.T,hidden_layer_delta)
        
def preprocessing(array):
    array = (array - array.min(axis=0))/(array.max(axis=0)- array.min(axis=0))
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
