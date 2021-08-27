# libraries:
import os 
from billiard import Process, Manager, Queue
# from multiprocessing import Process, Manager, Queue
import queue 
import itertools
import imagehash # used to create the hash
from PIL import Image # for openning and greyscaling the images
import copy


class phash():
    input_path = "/Users/hedayattabesh/Documents/scripts/Digital-Democracies-Instititute-Website/DDI_Website/ImageFlow/data/"
    output_path = "data/phashes.txt"
    image_extensions = ['.jpg', '.png', '.jpeg', '.gif']   # case-insensitive (upper/lower doesn't matter)
    identical = False
    
    def __init__(self, input_p="", output_p=""):
        if not input_p == "": self.input_path = input_p
        if not output_p == "": self.output_path = output_p
    

    # This function is meant to be used for multi-processes
    # It calculates the hash and cordinates with other processes using a Manager
    # It takes in a queue and a list derived from the Manager!
    # this function does not return anything as it is only meant to be used by computePhash
    def calculate_hash_func_df(self, in_queue, ns, results):
        # print(ns.df.at["file_name"])
        while True:
            # lets make sure the queue isnt empty!
            try:
                i = in_queue.get(True, 5)
            except queue.Empty: 
                break

            # now lets calculate the Hash!!
            # print("##")
            # print(ns.df.at[i, "file_name"])
            imgPhash = imagehash.phash(Image.open(ns.df.at[i, "abs_file_path"]))
            # this version uses greyscale to remove colors!
            imgPhash_gs = imagehash.phash(Image.open(ns.df.at[i, "abs_file_path"]).convert('LA'))

            # lets store into shared list for output
            results.append([i, str(imgPhash), str(imgPhash_gs)])

            
            
    # this function will calculate the phash for each image!
    # It takes in a list of images and with the power of multi-processing it computes all phashes
    # it write it all into output_path and returns True if successful
    def computePhash_df(self, df, max_size=8):
        # lets add the columns to the DF
        df["PHash"] = ""
        df["PHash_gs"] = ""
        print(len(df))
        with Manager() as manager:
            results = manager.list()
            work = manager.Queue()

            # lets add something to control what each proccess should do
            for i in range(len(df)):
                work.put(i)

            ns = manager.Namespace()
            ns.df = df

            # start for workers    
            out = []
            for i in range(max_size):
                print(i)
                p = Process(target=self.calculate_hash_func_df, args=(work, ns, results))
                p.start()
                out.append(p)
            
            # lets wait for the subprocesses
            for p in out:
                p.join()

            for i in results:
                df.at[i[0], "PHash"] = i[1]
                df.at[i[0], "PHash_gs"] = i[2]

            return df






