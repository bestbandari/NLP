import sys,os
import json

from parse import *
from replace import list_rare

# task 1: generate the rare word list for unseen words.
def task_1():
# generate initial count
    cmd = 'python count_cfg_freq.py ./data/parse_train.dat > ./data/cfg.counts'
    os.system(cmd)

# mark the rare words as "_rare_"
    cmd = 'python replace.py ./data/parse_train.dat ./data/cfg.counts > ./data/new_train.dat'
    os.system(cmd)

# regenerate count file    
    cmd = 'python count_cfg_freq.py ./data/new_train.dat > ./data/cfg_new.counts'
    os.system(cmd)

# generate the rare list
    list_rare('./data/cfg_new.counts', './data/list_rare.counts');

# task 2: compute the grammatical structure of sentences.
def task_2():
    parse_file('./data/parse_dev.dat', './data/cfg_new.counts', './data/parse_dev.out')
    parse_file('./data/try.dat', './data/cfg_new.counts', './data/try.out')
    
    cmd = 'python pretty_print_tree.py ./data/parse_dev.out > ./data/parse_dev.read'
    os.system(cmd) 
    
    cmd = 'python eval_parser.py ./data/try.key ./data/try.out'
    os.system(cmd)     
    
#the main function
if __name__=='__main__':
    task_1()
    
    task_2()

    
