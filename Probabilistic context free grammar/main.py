import sys,os
import pickle
import json

from parse import *
from replace import list_rare

# the process of task 1
def task_1():
# generate initial count
    cmd = 'python ./PA3_data/count_cfg_freq.py ./PA3_data/parse_train.dat > ./PA3_data/cfg.counts'
    os.system(cmd)

# replace the rare words   
    cmd = 'python replace.py ./PA3_data/parse_train.dat ./PA3_data/cfg.counts > ./PA3_data/new_train.dat'
    os.system(cmd)

# regenerate count file    
    cmd = 'python ./PA3_data/count_cfg_freq.py ./PA3_data/new_train.dat > ./PA3_data/cfg_new.counts'
    os.system(cmd)

# generate the easy readable file
    cmd = 'python ./PA3_data/pretty_print_tree.py ./PA3_data/new_train.dat > ./PA3_data/tree.read'
    os.system(cmd) 

# generate the rare list
    list_rare('./PA3_data/cfg_new.counts', './PA3_data/list_rare.counts');

# the process of task 2
def task_2():
    parse('./PA3_data/parse_dev.dat', './PA3_data/cfg_new.counts', './PA3_data/parse_dev.out')
    parse('./PA3_data/try.dat', './PA3_data/cfg_new.counts', './PA3_data/try.out')
    
    cmd = 'python ./PA3_data/pretty_print_tree.py ./PA3_data/parse_dev.out > ./PA3_data/parse_dev.read'
    os.system(cmd) 
    
    
#the main function
if __name__=='__main__':
    task_1()
    
    task_2()

    
