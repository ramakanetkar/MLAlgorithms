import sys
import math

def main():
    accepted_values = ["democrat", "A", "y", "before1950", "yes", "morethan3min", "fast", "expensive",
	            "high", "Two", "large","+"]
    #train_set = open("example2.csv","r")
    train_set = open (sys.argv[1],"r")
    #test_set = open("example1.csv","r")
    test_set = open (sys.argv[2],"r")
    test_headers = test_set.readline().rstrip().split(',')
    headers = train_set.readline().rstrip().split(',')
    node, pos_node, neg_node, pos_pos_node, pos_neg_node, neg_pos_node, neg_neg_node = None,None,None,None,None,None,None
    dataset = []
    for f in train_set:
        line = f.rstrip()
        dataset.append(line.split(','))
    index_list = [x for x in range(len(headers)-1)]
    node = get_node(dataset, accepted_values, -1, headers ,index_list)
    if node['gain'] > 0.1 and node['next_val'] != 'NA':
        pos_set = []
        neg_set = []
        for d in dataset:
            if d[node['next_index']] in accepted_values:
                pos_set.append(d)
            else:
                neg_set.append(d)
        index_list = [x for x in index_list if x != node['next_index']]
        pos_node = get_node(pos_set, accepted_values, node['next_index'], headers ,index_list)
        neg_node = get_node(neg_set, accepted_values, node['next_index'], headers ,index_list)
        if pos_node['gain'] > 0.1 and pos_node['next_val'] !='NA':
            pos_pos_set = []
            pos_neg_set = []
            for d in pos_set:
                if d[pos_node['next_index']] in accepted_values:
                    pos_pos_set.append(d)
                else:
                    pos_neg_set.append(d)
            index_list = [x for x in index_list if x != pos_node['next_index']]
            pos_pos_node = get_node(pos_pos_set, accepted_values, pos_node['next_index'], headers ,index_list)
            pos_neg_node = get_node(pos_neg_set, accepted_values, pos_node['next_index'], headers ,index_list)
        if neg_node['gain'] > 0.1 and neg_node['next_val']!='NA':
            neg_pos_set = []
            neg_neg_set = []
            for d in neg_set:
                if d[neg_node['next_index']] in accepted_values:
                    neg_pos_set.append(d)
                else:
                    neg_neg_set.append(d)
            index_list = [x for x in index_list if x != neg_node['next_index']]
            neg_pos_node = get_node(neg_pos_set, accepted_values, neg_node['next_index'], headers ,index_list)
            neg_neg_node = get_node(neg_neg_set, accepted_values, neg_node['next_index'], headers ,index_list)
    if node != None:
        print('[' + str(node['positive_count']) + '+/' + str(node['negative_count']) + '-]')
        print(node['next_val'] + '=y: ['+ str(pos_node['positive_count']) + '+/' + str(pos_node['negative_count']) + '-]')
        if pos_node != None:
            if pos_pos_node != None:
                print('| ',end="")
                print(pos_node['next_val'] + '=y: ['+ str(pos_pos_node['positive_count']) + '+/' + str(pos_pos_node['negative_count']) + '-]')
            if pos_neg_node != None:
                print('| ',end="")
                print(pos_node['next_val'] + '=n: ['+ str(pos_neg_node['positive_count']) + '+/' + str(pos_neg_node['negative_count']) + '-]')
        print(node['next_val'] + '=n: ['+ str(neg_node['positive_count']) + '+/' + str(neg_node['negative_count']) + '-]')
        if neg_node != None:
            if neg_pos_node !=None:
                print('| ',end="")
                print(neg_node['next_val'] + '=y: ['+ str(neg_pos_node['positive_count']) + '+/' + str(neg_pos_node['negative_count']) + '-]')
            if neg_neg_node !=None:
                print('| ',end="")
                print(neg_node['next_val'] + '=n: ['+ str(neg_neg_node['positive_count']) + '+/' + str(neg_neg_node['negative_count']) + '-]')
    train_error = 0
    for d in dataset:
        if node != None and node['next_val'] != 'NA':
            if d[headers.index(node['next_val'])] in accepted_values:
                if pos_node!= None and pos_node['next_val'] != 'NA':
                    if pos_pos_node == None and pos_neg_node == None:
                        if pos_node['positive_count'] >= pos_node['negative_count'] and d[-1] not in accepted_values:
                            train_error = train_error+1
                        elif pos_node['positive_count'] < pos_node['negative_count'] and d[-1] in accepted_values:
                            train_error = train_error+1
                    else:
                        if d[headers.index(pos_node['next_val'])] in accepted_values:
                            #pos_pos_node
                            if pos_pos_node != None:# and  pos_pos_node['next_val'] != 'NA':
                                #test error
                                if pos_pos_node['positive_count'] >= pos_pos_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif pos_pos_node['positive_count'] < pos_pos_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
                        else:
                            #pos_neg_node
                            if pos_neg_node != None:# and  pos_neg_node['next_val'] != 'NA':
                                #test error
                                if pos_neg_node['positive_count'] >= pos_neg_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif pos_neg_node['positive_count'] < pos_neg_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
            else:
                if neg_node != None and neg_node['next_val'] !='NA':
                    if neg_pos_node == None and neg_neg_node == None:
                        if neg_node['positive_count'] >= neg_node['negative_count'] and d[-1] not in accepted_values:
                            train_error = train_error+1
                        elif neg_node['positive_count'] < neg_node['negative_count'] and d[-1] in accepted_values:
                            train_error = train_error+1
                    else:
                        if d[headers.index(neg_node['next_val'])] in accepted_values:
                            #neg_pos_node
                            if neg_pos_node != None:# and  neg_pos_node['next_val'] != 'NA':
                                #test error
                                if neg_pos_node['positive_count'] >= neg_pos_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif neg_pos_node['positive_count'] < neg_pos_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
                        else:
                            #neg_neg_node
                            if neg_neg_node != None:# and  neg_neg_node['next_val'] != 'NA':
                                #test error
                                if neg_neg_node['positive_count'] >= neg_neg_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif neg_neg_node['positive_count'] < neg_neg_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
    print("error(train): " + str(train_error/len(dataset)))
    train_error = 0
    testing_dataset = []
    for f in test_set:
        line = f.rstrip()
        testing_dataset.append(line.split(','))
    for d in testing_dataset:
        if node != None and node['next_val'] != 'NA':
            if d[headers.index(node['next_val'])] in accepted_values:
                if pos_node!= None and pos_node['next_val'] != 'NA':
                    if pos_pos_node == None and pos_neg_node == None:
                        if pos_node['positive_count'] >= pos_node['negative_count'] and d[-1] not in accepted_values:
                            train_error = train_error+1
                        elif pos_node['positive_count'] < pos_node['negative_count'] and d[-1] in accepted_values:
                            train_error = train_error+1
                    else:
                        if d[headers.index(pos_node['next_val'])] in accepted_values:
                            #pos_pos_node
                            if pos_pos_node != None: #and  pos_pos_node['next_val'] != 'NA':
                                #test error
                                if pos_pos_node['positive_count'] >= pos_pos_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif pos_pos_node['positive_count'] < pos_pos_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
                        else:
                            #pos_neg_node
                            if pos_neg_node != None: #and  pos_neg_node['next_val'] != 'NA':
                                #test error
                                if pos_neg_node['positive_count'] >= pos_neg_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif pos_neg_node['positive_count'] < pos_neg_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
            else:
                if neg_node != None and neg_node['next_val'] !='NA':
                    if neg_pos_node == None and neg_neg_node == None:
                        if neg_node['positive_count'] >= neg_node['negative_count'] and d[-1] not in accepted_values:
                            train_error = train_error+1
                        elif neg_node['positive_count'] < neg_node['negative_count'] and d[-1] in accepted_values:
                            train_error = train_error+1
                    else:
                        if d[headers.index(neg_node['next_val'])] in accepted_values:
                            #neg_pos_node
                            if neg_pos_node != None: #and  neg_pos_node['next_val'] != 'NA':
                                #test error
                                if neg_pos_node['positive_count'] >= neg_pos_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif neg_pos_node['positive_count'] < neg_pos_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
                        else:
                            #neg_neg_node
                            if neg_neg_node != None: #and  neg_neg_node['next_val'] != 'NA':
                                #test error
                                if neg_neg_node['positive_count'] >= neg_neg_node['negative_count'] and d[-1] not in accepted_values:
                                    train_error = train_error+1
                                elif neg_neg_node['positive_count'] < neg_neg_node['negative_count'] and d[-1] in accepted_values:
                                    train_error = train_error+1
    print("error(test): " + str(train_error/len(testing_dataset)))
    train_set.close()
    test_set.close()

def get_node(dataset, accepted_values, attribute_index, headers, index_list):
    positive_count = 0
    negative_count = 0
    node = {}
    for d in dataset:
        if d[-1] in accepted_values:
            positive_count = positive_count+1
        else:
            negative_count = negative_count + 1
    node['positive_count'] = positive_count
    node['negative_count'] = negative_count
    node['entropy'] = calculate_entropy(positive_count,negative_count)
    node['next_val'] ='NA'
    node['gain'] = 1
    if len(index_list) == 0:
        return node
    else:
        node['gain'],next_index = get_next_node(node['entropy'], dataset, accepted_values, index_list)
        node['next_val'] = headers[next_index]
        node['next_index'] = next_index
        return node
    
def get_next_node(entropy, dataset, accepted_values, index_list):
    gain= {}
    entrophy = {}
    if True:
        for i in index_list:
    ##        print(i)
            temp_pos = []
            temp_neg = []
            temp_pos_pcount, temp_pos_ncount,temp_neg_pcount, temp_neg_ncount = 0,0,0,0
            for d in dataset:
    ##            print(d)
                if d[i] in accepted_values:
                    temp_pos.append(d)
                else:
                    temp_neg.append(d)
            temp_pos_pcount, temp_pos_ncount = get_pos_neg_count(temp_pos,accepted_values)
            ep = len(temp_pos)/len(dataset) * calculate_entropy(temp_pos_pcount, temp_pos_ncount)
            temp_neg_pcount, temp_neg_ncount = get_pos_neg_count(temp_neg,accepted_values)
            en = len(temp_neg)/len(dataset) * calculate_entropy(temp_neg_pcount, temp_neg_ncount)
            gain[i] = (entropy-ep-en)
            entrophy[i] = (ep+en)
        return max(gain.values()), [i for i,value in gain.items() if value == max(gain.values())][0]
    else:
        return None
            
def get_pos_neg_count (input_data, accepted_values):
    pos_count = 0
    neg_count = 0
    for i in input_data:
        if i[-1] in accepted_values:
            pos_count =pos_count+1
        else:
            neg_count =neg_count+1
    return pos_count, neg_count
def calculate_entropy(plus,minus):
    if True:
        total = plus + minus
        if plus == 0 and minus == 0:
            return 0
        elif plus == 0 and minus !=0:
            return (minus/total) * math.log((total/minus),2)
        elif plus !=0 and minus == 0:
            return (plus/total) * math.log((total/plus),2)
        else:
            xp = (plus/total) * math.log((total/plus),2)
            xm = (minus/total) * math.log((total/minus),2)
            return xp + xm
if __name__=="__main__":
    main()
