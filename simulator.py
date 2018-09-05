import time
import datetime
from tzlocal import get_localzone
from pymongo import MongoClient 
import random
import matplotlib.pyplot as plt

import numpy as np
import scipy
from scipy.stats import powerlaw

client = MongoClient("mongodb://localhost:27017")
db = client['metadata1']
#collection = db['uniform']
collection = db['randomSize']
f = open('smartPolicy2.csv', 'w')
f2 = open('mean2.csv', 'w')
sim_results = open('sim_results2.csv', 'w')
mean = 0


'''
Formula : Time, Cost
HOT Formula :  x, y
COLD Formula : 100x, 5y
'''

'''
def simulator():
    print "Simulator!"
    tier = -1
    for i in range(0,20000):
        obj = random.randint(0, 1000)
        cur = collection.find({"objectID" : obj})
        collection.update_one({'objectID': obj}, {'$inc': {'accessFreq': 1}})
        #o = cur.next()
        #tier = o["tier"]
        #size = o["size"]
        #if tier == 1:
        #    f.write(str(1 * size) + '\n')
'''

'''
def simulator():
    print "Simulator!"
    tier = -1
    hot_read_time = 0
    hot_write_time = 0
    cold_read_time = 0
    cold_write_time = 0
    
    hot_read_size = 0
    hot_write_size = 0
    cold_read_size = 0
    cold_write_size = 0

    hot_read_list = list()
    hot_write_list = list()
    cold_read_list = list()
    cold_write_list = list()

    for i in range(0,20000):
        obj = random.randint(0, 999)
        cur = collection.find({"objectID" : obj})
    
        #print i, "  -- ", obj
        #print cur
        o = cur.next()
        #print o
    
        request_type = random.randint(0, 100) # 30-70 partition
        if request_type < 70: # Read
            # DO READ SHIT
            if o["tier"] == 1: # COLD
                # COLD & READ
                cold_read_time += o["size"] * 2 

                if obj not in cold_read_list:
                    cold_read_list.append(obj)
                    cold_read_size += o["size"]


            else: # HOT
                # HOT & READ
                hot_read_time += o["size"] * 1

                if obj not in hot_read_list:
                    hot_read_list.append(obj)
                    hot_read_size += o["size"]

        else: # Write
            # DO WRITE SHIT
            if o["tier"] == 1: # COLD
                # COLD & WRITE
                cold_write_time += o["size"] * 3

                if obj not in cold_write_list:
                    cold_write_list.append(obj)
                    cold_write_size += o["size"]

            else: # HOT
                # HOT & WRITE
                hot_write_time += o["size"] * 1.5

                if obj not in hot_write_list:
                    hot_write_list.append(obj)
                    hot_write_size += o["size"]


    print "HOT Read Time", hot_read_time
    print "HOT Write Time", hot_write_time
    print "COLD Read Time", cold_read_time
    print "COLD Write Time", cold_write_time

    print "--------------------------------"

    print "HOT Read Size", hot_read_size
    print "HOT Write Size", hot_write_size
    print "COLD Read Size", cold_read_size
    print "COLD Write Size", cold_write_size
'''

# PowerLaw Sim
def pl_simulator():
    print "Power Law Sim"
    r = scipy.stats.powerlaw.rvs(10, loc = 0, scale = 1000, size = 20000)
    hot_time = 0
    cold_time = 0
    
    hot_size = 0
    cold_size = 0

    hot_list = list()
    cold_list = list()
    for i in r:
        obj = int(i)
        cur = collection.find({"objectID" : obj})
        o = cur.next()

        collection.update_one({'objectID': obj}, {'$inc': {'accessFreq': 1}})

        tier = o["tier"]
        size = o["size"]
        if tier == 1:
            # COLD STUFF
            cold_time += size * 2
            if obj not in cold_list:
                cold_list.append(obj)
                cold_size += size
        if tier == 2:
            # HOT STUFF
            hot_time += size * 1
            if obj not in hot_list:
                hot_list.append(obj)
                hot_size += size
            
    print "Hot Time : ",hot_time
    print "Hot Size : ",hot_size 
    print "Cold Time : ",cold_time
    print "Cold Size : ",cold_size


def plot_graph():
    points = list()
    objs = collection.find({})
    for i in objs:
        af = i["accessFreq"]
        points.append(af)
        f.write( str(af) + '\n')
    
    plt.plot(points)
    plt.show()


def freq_count():
    tier1_freq = 0
    tier2_freq = 0
    tier1_total_size = 0
    tier2_total_size = 0
    objs = collection.find({})
    for i in objs:
        af = i["accessFreq"]
        tier = i["tier"]
        size = i["size"]
        
        if tier==1:
            #DO TIER 1 COLD stuff
            tier1_freq += af * size
            tier1_total_size += size
            f.write( str(size) + ',' + str(af * size * 5) + '\n')
        else:
            # Tier 2 HOT
            tier2_freq += af * size
            tier2_total_size += size
            f.write( str(size) + ',' + str(af * size) + '\n')

    print "Tier 1 total bytes transferred :", tier1_freq
    print "Tier 1 total size :", tier1_total_size
    print "Tier 2 total bytes transferred :", tier2_freq
    print "Tier 2 total size :", tier2_total_size


def accessFreq_distro(c):
    # access freq ka chutiyapa
    objs = collection.find({})
    freq=0
    global mean
    hot_size = 0
    hot_list = list()
    cold_size = 0
    cold_list = list()
    mean = 0
    for i in objs:
        af = i["accessFreq"]
        objID = i["objectID"]
        f.write(str(af)+ ",")
        freq += int(af)
        if i['tier'] > 1:
            if objID not in hot_list:
                hot_list.append(objID)
                hot_size += i['size']
        else:
            if objID not in cold_list:
                cold_list.append(objID)
                cold_size += i['size']
        

    print "Hot Size: ", hot_size
    print "Cold Size: ", cold_size
    mean = float(freq)/float(c)
    #print "C : ",  c
    #print "Freq Total : ", freq
    #print "Mean : ", mean
    f2.write(str(mean) + "\n")
    hot_to_cold = collection.update_many({'accessFreq': {'$lt' : mean}}, {'$set': {'tier': 1}})
    cold_to_hot = collection.update_many({'accessFreq': {'$gt' : mean}}, {'$set': {'tier': 2}})

    print "Hot to cold matched : ", hot_to_cold.matched_count
    print "Hot to cold modified : ", hot_to_cold.modified_count
    print "Cold to Hot matched : ", cold_to_hot.matched_count
    print "Cold to Hot modified : ", cold_to_hot.modified_count
    f.write("\n")

    return hot_size, cold_size



def smart_simulation():
    print "SMart Sim"
    r = scipy.stats.powerlaw.rvs(10, loc = 0, scale = 1000, size = 20000)
    hot_time = 0
    cold_time = 0
    hot_size = 0
    cold_size = 0

    hot_list = list()
    cold_list = list()

    count=0

    for i in r: # 20000 Loop
        count += 1
        obj = int(i)
        cur = collection.find({"objectID" : obj})
        o = cur.next()

        collection.update_one({'objectID': obj}, {'$inc': {'accessFreq': 1}})

        tier = o["tier"]
        size = o["size"]
        if tier == 1:
            # COLD STUFF
            cold_time += size * 2
            if obj not in cold_list:
                cold_list.append(obj)
                cold_size += size
        if tier == 2:
            # HOT STUFF
            hot_time += size * 1
            if obj not in hot_list:
                hot_list.append(obj)
                hot_size += size


        if count%500 == 0:
            # HOT TIME, HOT SIZE, COLD TIME, COLD SIZE
            hot_tier_size, cold_tier_size = accessFreq_distro(count)
            sim_results.write( str(hot_tier_size) + ", " + str(cold_tier_size) + ", " + str(hot_time) + ", " + str(hot_size) + ", " + str(cold_time) + ", " + str(cold_size) + "\n")
            hot_time = 0
            cold_time = 0
            hot_size = 0
            cold_size = 0
            hot_list = list()
            cold_list = list()
            
    
    print "Hot Time : ",hot_time
    print "Hot Size : ",hot_size 
    print "Cold Time : ",cold_time
    print "Cold Size : ",cold_size 


def main():
    print "Hello World!"
    random.seed(0)
    #pl_simulator()
    smart_simulation()
    #plot_graph()
    #freq_count()

    '''
    objs = collection.find({})
    for i in objs:
        af = i["accessFreq"]
        objID = i["objectID"]
        f.write(str(objID) + "," + str(af) + "\n")
    
    objs = collection.find({})
    size = 0
    for i in objs:
        size += i["size"]


    print "Avg size of 1000 objects : ", (size)
    
    objs = collection.find({})
    for i in objs:
        print i
    '''

if __name__ == '__main__':
    main()