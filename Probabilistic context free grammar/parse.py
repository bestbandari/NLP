import sys,json

#generate the vovabulary of frequency higher or equal to 5
def vocabulary(file):
    f = open(file, 'r')
    v = set()
    
    for line in f:
        token = line.split()
        if  token[1] == 'UNARYRULE' and int(token[0]) >=5 :
            v.add(token[3])
    
    f.close()
    return v

# add a value to binary rule. The varible is a 3-layer dictionary structure
def add_binary(count_yz_x, x, y, z, num):
    #if the key does not exist, create a one.
    if  y not in count_yz_x:
        count_yz_x[y] = {}  
    
    #if the key does not exist, create a one.
    if  z not in count_yz_x[y]:
        count_yz_x[y][z] = {}
        
    count_yz_x[y][z][x] = int(num)

# add a value to unary rule. The varible is a 2-layer dictionary structure
def add_unary(count_y_x, x, y, num):
    #if the key does not exist, create a one.
    if  y not in count_y_x:
        count_y_x[y] = {}
    
    count_y_x[y][x] = int(num)

# add a value to nonterminal. The varible is a 1-layer dictionary structure
def add_nonterm(count_x, x, num):
    count_x[x] = int(num)

# generate the parameters to CKY algorithm. Use multilayer dictionary to store these parameters.
def train(file):
    f = open(file, 'r')
    
    # count of nonterminals
    count_x = {}
    # count of unary rule that x->y
    count_y_x = {}
    # count of binary rule that x->yz
    count_yz_x = {}
    
    # init count
    for line in f:
        token = line.split()
        if  token[1] == 'NONTERMINAL':
            add_nonterm(count_x, token[2], token[0])
        
        if  token[1] == 'UNARYRULE':
            add_unary(count_y_x, token[2], token[3], token[0])
        
        if  token[1] == 'BINARYRULE':
            add_binary(count_yz_x, token[2], token[3], token[4], token[0])
    
    # generate probabilities for x->y
    for y in count_y_x:
        for x in count_y_x[y]:
            count_y_x[y][x] = count_y_x[y][x] / count_x[x]
    
    # generate probabilities for x->yz    
    for y in count_yz_x:
        for z in count_yz_x[y]:
            for x in count_yz_x[y][z]:
                count_yz_x[y][z][x] = count_yz_x[y][z][x] / count_x[x]
                
    
    f.close()
    return count_y_x, count_yz_x

# add values to CKY varibles, including pi and backpoint
def add_CKY(pi, bp, i, j, x, value, s, y, z):
    if  i not in pi:
        pi[i] = {}
        bp[i] = {}
    if  j not in pi[i]:
        pi[i][j] = {}
        bp[i][j] = {}
    if  x not in pi[i][j]:
        pi[i][j][x] = value
        bp[i][j][x] = [s, y, z]
    elif  value > pi[i][j][x]:
        pi[i][j][x] = value
        bp[i][j][x] = [s, y, z]

# return the word itself if it is in the vocabulary( of high frequency ), 
# return _rare_ otherwise(of low frequency or never seen)
def get_word(word, voc):
    if  word in voc:
        return word
    return '_rare_'

# check if a rule exists. if not exists, skip to next computation
def is_rule(q_yz_x, y, z):
    if  y in q_yz_x and z in q_yz_x[y] :
        return True
    
    return False

# check if a pi value exists. if not exists, skip to next computation
def is_pi(pi, i, s, j):
    if  i in pi and s in pi[i] and s+1 in pi and j in pi[s+1]:
        return True
    
    return False

# implementation of CKY algorithm
def CKY(words, voc, q_y_x, q_yz_x):
    pi = {}
    bp = {}
    n = len(words)
    
    # initialization
    for i in range(n):
        rule = q_y_x[get_word(words[i], voc)]
        for x in rule:
            add_CKY(pi, bp, i, i, x, rule[x], -1, words[i], [])
    
    # dynamic programming
    for l in range(n - 1):
        for i in range(n - l):
            j = i + l + 1
            for s in range(i, j):
                if  is_pi(pi, i, s, j):
                    for y in pi[i][s]:
                        for z in pi[s + 1][j]:
                            if  is_rule(q_yz_x, y, z):
                                for x in q_yz_x[y][z]:
                                    q = q_yz_x[y][z][x] * pi[i][s][y] * pi[s + 1][j][z] 
                                    add_CKY(pi, bp, i, j, x, q, s, y, z)
                                        
    return pi[0][n-1]['SBARQ'], bp

# recursively recover the parse tree from backpoint structure
def recover(bp, i, j, x):
    if  i == j:
        return [x, bp[i][j][x][1]]
    
    return [x, recover(bp, i, bp[i][j][x][0], bp[i][j][x][1]), recover(bp, bp[i][j][x][0] + 1, j, bp[i][j][x][2])]
    

# parse the file line by line
def parse(file_dev, file_count, file_out):
    fi = open(file_dev, 'r')
    fo = open(file_out, 'w')
    
    voc = vocabulary(file_count)
    q_y_x, q_yz_x = train(file_count)
    
    for line in fi:
        words = line.split()
        q, bp = CKY(words, voc, q_y_x, q_yz_x)
        tree = recover(bp, 0, len(words) - 1, 'SBARQ')
        js_tree = json.dumps(tree)
        fo.write(js_tree + '\n')
    
    fi.close()
    fo.close()