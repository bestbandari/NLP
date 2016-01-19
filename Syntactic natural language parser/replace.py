import sys,json

#generate rare list
def list_rare(file_rule, file_rare):
    fi = open(file_rule, 'r')
    fo = open(file_rare, 'w')

    #write the lines that involve rare to the output file
    for line in fi:
        token = line.split()
        if  token [1] == 'UNARYRULE' and token[3] == '_rare_':
            fo.write(line)
    
    fi.close()
    fo.close()
            
def dictionary_add_1(dic, key, value):
    if  key not in dic:
        dic[key] = value
    else:
        dic[key] += value

        
# find the rules of frequency lower than 5
def count_rare(file):
    count = {}
    rare = []
    f = open(file, 'r')
    
    # count frequency for each word
    for line in f.readlines():
        token = line.split()
        
        if  token[1] == 'UNARYRULE' :
            dictionary_add_1(count, token[3], int(token[0]))
    
    # list the infrequent words
    for word in count:
        if  count[word] < 3:
            rare.append(word)
    
    f.close()
    return rare

# recursively replace the rare words
def replace_tree(tree, rare):
    
    if  len(tree) == 2:
        # leaf node, replace rare if necessary
        if  tree[1] in rare:
            tree[1] = '_rare_'
    elif len(tree) == 3:
        # nonterminal, recur
        replace_tree(tree[1], rare)
        replace_tree(tree[2], rare)
    
if __name__=='__main__':
    if len(sys.argv) != 3:
        print 'error input'
        sys.exit(1)
    
    f_tree = sys.argv[1]
    f_count = sys.argv[2]

# get the rare words    
    rare = count_rare(f_count)

#replace rare words line by line
    fi = open(f_tree,'r')
    for line in fi:
        tree = json.loads(line)
        replace_tree(tree,rare)
        new_tree = json.dumps(tree)
        print new_tree
    fi.close()
    
    