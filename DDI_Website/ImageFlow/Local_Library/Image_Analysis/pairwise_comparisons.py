# This code uses a majority of the code found at: https://github.com/zsavvas/memes_pipeline
# The code was created as part ofxw "On the Origins of Memes by Means of Fringe Web Communities" at IMC 2018.
# This is just a Refactored version with the use of object oriented design
# While refactoring, upgraded code to run with latest version of libraries and python

# libraries:
import os
import json
import time
import threading
import pickle

import numpy as np
import sys
import distance
import json
import math
from billiard import Process, Manager, Queue

from scipy.sparse import csr_matrix

class pairwise_comparisons():
    input_path = "data/phashes_full.txt"
    output_dir = "/Users/hedayattabesh/Documents/scripts/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/"
    output_path = output_dir + "phashes-diffs.json"
    num_avail_proc = 1

    def __init__(self, identical, input_p="", output_p=""):
        if not input_p == "": self.input_path = input_p
        if not output_p == "": self.output_path = output_p
        if identical: self.DISTANCE_THRESHOLD = 0
        else: self.DISTANCE_THRESHOLD = 12

    def read_phashes_manifest(self):
        phashes = []
        with open(self.input_path) as infile:
            for line in infile.readlines():
                split = line.split('	')
                hashid = split[0].strip()
                hash_str = split[1].strip()
                phashes.append([hashid, hash_str])
        print('[i] processed', len(phashes))
        return phashes
    
    # this function is meant to be used with multiprocessing to run through calculating all the haming distances of the images
    def calculate_diff(self, phashes, shared_list, input_queue):
        # create a dictionary for output
        output = []
        while True:
            # lets see if input queue has items! If not then we are done!
            try:
                curr_i = input_queue.get(block=False)
            except:
                break
            print(curr_i)
            # now lets compare it to every other image!
            # by going to i+1 we can avoid duplicates since the bottom half of the matrix is the same as the top half!
            j = curr_i+1
            while j < len(phashes):
                # lets calculate the distance!
                ham_dist = distance.hamming(phashes[curr_i][1], phashes[j][1])
                # lets check if the distance is within our threshold
                if ham_dist <= self.DISTANCE_THRESHOLD:
                    # if so then lets add it to our output dic
                    # key = phashes[curr_i][0] + "-" + phashes[j][0]
                    output.append([[phashes[curr_i][0], phashes[j][0]], ham_dist])
                j = j + 1
        # finally lets append the results to the shared list to keep the information when processes is finished!
        shared_list.append(output)

    def compare(self, phashes=None):
        if phashes == None:
            phashes = self.read_phashes_manifest()

        # lets create a manager for passing shared resources between the processes
        manager = Manager()
        return_list = manager.list()
        input_queue = manager.Queue()
        
        # lets add all the i's to the input queue to make sure all processes are doing unique work
        for i in range(len(phashes)):
            input_queue.put(i)

        # lets create processes and run thorugh the calculations
        procs = []
        for i in range(self.num_avail_proc):
            proc = Process(target=self.calculate_diff, args=(phashes, return_list, input_queue))
            proc.start()
            procs.append(proc)
        
        # lets way for the processes to finish!
        for proc in procs:
            proc.join()

        # finally lets merge our dictionaries so that we can dump to a json
        final = return_list[0]
        if len(return_list) > 1:
            for item in final[1:]:
                final = final + item

        # with open(self.output_path, 'w') as outfile:
        #     json.dump(final_json, outfile)
        
        return final


