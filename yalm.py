import boto
import boto3
#from boto.s3.connection import S3Connection
from boto.s3.key import Key
import botocore

import operator
import time
import datetime
from datetime import date, timedelta
from tzlocal import get_localzone
from pymongo import MongoClient 
import random
import matplotlib.pyplot as plt

import numpy as np
import scipy
from scipy.stats import powerlaw

import mysql.connector

'''
c = boto.connect_s3()
b = c.get_bucket('yaml-s3', validate=False)
k = Key(b)
k.S
k.key = 'foobar2'
k.set_contents_from_filename('./file010.bin')
'''
'''
#s3 = boto3.resource('s3')
#s3.Object('yaml-s3', 'foobar3').put(Body=open('./file010.bin', 'rb'), StorageClass = 'STANDARD')


glacier = boto3.client('glacier', region_name='us-east-1')

glacier_r = boto3.resource('glacier', region_name = 'us-east-1')

file_to_upload = open('./tmp.txt', mode='rb')

response = glacier.upload_archive(
            vaultName='yaml-g',
            archiveDescription='TEMP TEXT',
            body=file_to_upload)



Tier = 0 = S3
Tier = 1 = Glacier


'''

policy_interval = 500

cnx = mysql.connector.connect(user='yaml', password='helloworld',host='metadata1.c4swc7cef0fm.us-east-1.rds.amazonaws.com',database='MetadataYAML')
cursor = cnx.cursor()

s3 = boto3.resource('s3')
hot_bucket = 'yaml-s3'
cold_bucket = 'yaml-g'

f = open('awsSim_' + str(datetime.datetime.now()) + '.csv', 'w')
f.write('key' + ',' + 'req_time' + ',' + 'size' + ", time_size"+ '\n')

cf = open('clusterFile_' + str(datetime.datetime.now()) + '.csv', 'w')
cf.write('key' + ',' + 'accessFreq' + ',' + 'size' + ',' + 'accessTime' + '\n')

debugFile = open('debugFile_' + str(datetime.datetime.now()) + '.csv', 'w')

debugSimFile = open('debugSimFile_' + str(datetime.datetime.now()) + '.csv', 'w')

coldDataFile = open('coldDataFile_' + str(datetime.datetime.now()) + '.csv', 'w')

bucketMetrics = open('bucketMetrics_' + str(datetime.datetime.now()) + '.csv', 'w')
bucketMetrics.write("Hot_Size_b, Hot_Objs_b, Cold_Size_b, Cold_Objs_b, Hot_Size_a, Hot_Objs_a, Cold_Size_a, Cold_Objs_a, time_size \n")

tmpDebugFile = open('tmpDebugFile_' + str(datetime.datetime.now()) + '.csv', 'w')

deltaFile = open('deltaFile_' + str(datetime.datetime.now()) + '.csv', 'w')

no_of_objs = 0
cold_to_hot_list = list()

delta_list = list()

def populateMySql():
    bucket = s3.Bucket(hot_bucket)

    add_obj = ("INSERT INTO `MetadataTable` "
               "(ObjId, Size, CreationTime, LastModified, Acessfrq) "
               "VALUES (%s, %s, %s, %s, %s)")

    for key in bucket.objects.all():
        data_obj = (key.key, key.size, key.last_modified, key.last_modified, 0)
        cursor.execute(add_obj, data_obj)
        cnx.commit()


def get_bucket_metrics():
    # HOT BUCKET METRICS
    hot_bucketMetrics_size = 0
    hot_bucketMetrics_objs = 0
    for key in s3.Bucket(hot_bucket).objects.all():
        hot_bucketMetrics_size += key.size
        hot_bucketMetrics_objs += 1
    # COLD BUCKET METRICS
    global cold_to_hot_list
    
    cold_to_hot_list[:] = []
    cold_bucketMetrics_size = 0
    cold_bucketMetrics_objs = 0
    for key in s3.Bucket(cold_bucket).objects.all():
        cold_bucketMetrics_size += key.size
        cold_bucketMetrics_objs += 1
        cold_to_hot_list.append(key.key)
    bucketMetrics.write(str(hot_bucketMetrics_size) + " ," + str(hot_bucketMetrics_objs) + ", " + str(cold_bucketMetrics_size) + ", " +str(cold_bucketMetrics_objs))
    global no_of_objs
    no_of_objs = cold_bucketMetrics_objs * 0.10
    

def move_from_cold_to_hot_with_delta(accessTime):
    # MOVE FROM DELTA
    global delta_list

    # FIND MEAN OF DELTA LIST AND DO STUFF

    delta_mean = float(sum(delta_list))/len(delta_list)

    ###
    for k,v in accessTime.iteritems():
        tmpDebugFile.write("k,v : " + str(k) + " -- " + str(v) + "\n" )

    #cold_accessTime_list = [k,v for k,v in accessTime.iteritems() if k in cold_to_hot_list]

    cold_accessTime_list = list()

    for k,v in accessTime.iteritems():
        if k in cold_to_hot_list:
            cold_accessTime_list.append((k,v))

    #sorted_accessTime = sorted(accessTime.items(), key=operator.itemgetter(1))

    cold_accessTime_list = sorted(cold_accessTime_list, key=lambda tup: tup[1])

    tmpDebugFile.write("AFTER SORT cold_accessTime_list\n" )
    for k,v in cold_accessTime_list:
        tmpDebugFile.write("k,v : " + str(k) + " -- " + str(v) + "\n" )

    count = 0
    for key,j in cold_accessTime_list:
        # Based on delta : MOVE key to HOT
        current_time = datetime.datetime.now()

        delta = current_time - j

        delta = delta.total_seconds()

        if delta < delta_mean:
            continue

        # ELSE move to Hot

        debugFile.write("\n")
        debugFile.write("Key : " + key + "   , Access-Value : " + str(j) + "   ---- MOVING TO HOT BUCKET")
        copy_source = {
                'Bucket': cold_bucket,
                'Key': key
            }
        destBucket = s3.Bucket(hot_bucket)
        destBucket.copy(copy_source, key)
        re = s3.Object(cold_bucket, key).delete() # Delete from Hot Bucket
        if re['ResponseMetadata']['HTTPStatusCode'] != 204:
            print re
            exit(0)
        # Update MetaDataTable
        cursor.execute("UPDATE `MetadataTable` SET Tier = 0 WHERE `ObjId` = '" +  key + "'")
        cnx.commit()
        count += 1
        if count >= no_of_objs:
            return


def move_from_cold_to_hot(accessTime): # MOVE FROM COLD TO HOT
    global no_of_objs
    debugFile.write("MOVING FROM COLD TO HOT\n")
    debugFile.write("no_of_objs is : " + str(no_of_objs) + "\n\n")
    debugFile.write("MOVING IS... ::: \n\n")

    tmpDebugFile.write("BEFORE SORT accessTime\n" )
    for k,v in accessTime.iteritems():
        tmpDebugFile.write("k,v : " + str(k) + " -- " + str(v) + "\n" )

    #cold_accessTime_list = [k,v for k,v in accessTime.iteritems() if k in cold_to_hot_list]

    cold_accessTime_list = list()

    for k,v in accessTime.iteritems():
        if k in cold_to_hot_list:
            cold_accessTime_list.append((k,v))

    #sorted_accessTime = sorted(accessTime.items(), key=operator.itemgetter(1))

    cold_accessTime_list = sorted(cold_accessTime_list, key=lambda tup: tup[1])

    tmpDebugFile.write("AFTER SORT cold_accessTime_list\n" )
    for k,v in cold_accessTime_list:
        tmpDebugFile.write("k,v : " + str(k) + " -- " + str(v) + "\n" )

    count = 0
    for key,j in cold_accessTime_list:
        # MOVE key to HOT
        debugFile.write("\n")
        debugFile.write("Key : " + key + "   , Access-Value : " + str(j) + "   ---- MOVING TO HOT BUCKET")
        copy_source = {
                'Bucket': cold_bucket,
                'Key': key
            }
        destBucket = s3.Bucket(hot_bucket)
        destBucket.copy(copy_source, key)
        re = s3.Object(cold_bucket, key).delete() # Delete from Hot Bucket
        if re['ResponseMetadata']['HTTPStatusCode'] != 204:
            print re
            exit(0)
        # Update MetaDataTable
        cursor.execute("UPDATE `MetadataTable` SET Tier = 0 WHERE `ObjId` = '" +  key + "'")
        cnx.commit()
        count += 1
        if count >= no_of_objs:
            return


def move_data(mi, miDict): # MOVE DATA FROM HOT TO COLD
    debugFile.write("Mi is : " + str(mi) + "\n\n")
    debugFile.write("MI DICT IS ::: \n\n")
    for key, miValue in miDict.iteritems():
        debugFile.write("\n")
        debugFile.write("Key : " + key + "   , Mi-Value : " + str(miValue) + "     ")
        if miValue > mi:
            #CHANGE KEY TIER TO GLACIER (1)
            debugFile.write(" -- Moving to COLD BUCKET")
            # MOVE
            copy_source = {
                'Bucket': hot_bucket,
                'Key': key
            }
            destBucket = s3.Bucket(cold_bucket)
            destBucket.copy(copy_source, key)
            re = s3.Object(hot_bucket, key).delete() # Delete from Hot Bucket
            if re['ResponseMetadata']['HTTPStatusCode'] != 204:
                print re
                exit(0)
            # Update MetaDataTable
            cursor.execute("UPDATE `MetadataTable` SET Tier = 1 WHERE `ObjId` = '" +  key + "'")
            cnx.commit()
            

def aws_simulation():
    print "SMart Sim"
    r = scipy.stats.powerlaw.rvs(10, loc = 0, scale = 1000, size = 20000)
    hot_time = 0
    cold_time = 0
    hot_size = 0
    cold_size = 0

    hot_list = list()
    cold_list = list()

    accessFreq = dict()
    accessTime = dict()
    sizeToWrite = dict()

    cfList = list()

    mi = 0.0 # Movement Index

    miDict = dict()

    count=0

    time_size = 0

    for i in r: # 20000 Loop
        print count, ".."
        count += 1
        num = '%03d' % i
        key = 'file' + num + '.bin'

        # GET OBJECT's Bucket

        cursor.execute("SELECT `Tier` FROM `MetadataTable` WHERE `ObjId` = '" +  key + "'")

        bucket_results = cursor.fetchall()

        obj_bucket = 0    
        for b in bucket_results:
            obj_bucket = b[0]

        #print obj_bucket

        req_time = 300  # Penalty for obj being in cold
        aws_bucket = cold_bucket

        if obj_bucket == 0:
            aws_bucket = hot_bucket
            req_time = 0 # Remove the penalty
        
        start_time = time.time()

        try:
            s3.Bucket(aws_bucket).download_file(key, './tmp/' + key)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist. : ", key)
            else:
                raise

        req_time += (time.time() - start_time)

        # IF in cold... Move to s3 (hot)
        if aws_bucket == cold_bucket:
            debugSimFile.write("\n")
            debugSimFile.write("Key : " + key + "     ----- Moving to Hot  ----- " + str(datetime.datetime.now()))
            # Moving to Hot
            copy_source = {
                'Bucket': cold_bucket,
                'Key': key
            }
            destBucket = s3.Bucket(hot_bucket)
            destBucket.copy(copy_source, key)
            re = s3.Object(cold_bucket, key).delete() # Delete from Hot Bucket
            if re['ResponseMetadata']['HTTPStatusCode'] != 204:
                print re
                exit(0)
            # Update MetaDataTable
            cursor.execute("UPDATE `MetadataTable` SET Tier = 0 WHERE `ObjId` = '" +  key + "'")
            cnx.commit()
            

        global delta_list

        if key not in accessFreq:
            accessFreq[key] = 1
        else:
            accessFreq[key] += 1

        old_time = 0

        if key in accessTime:
            old_time = accessTime[key]

        accessTime[key] = datetime.datetime.now()

        if aws_bucket == cold_bucket:
            delta = accessTime[key] - old_time # datetime.timedelta
            print type(delta)
            print delta
            delta = delta.total_seconds()
            print "----------"
            print type(delta)
            print delta
            deltaFile.write(key + "," + str(delta) + "\n")
            delta_list.append(delta)
    
        cursor.execute("SELECT `Size` FROM `MetadataTable` WHERE `ObjId` = '" +  key + "'")

        results = cursor.fetchall()

        for size in results:
            sizeToWrite[key] = size[0]

        '''
        if key not in cfList:
            cf.write(key + ',' + str(accessFreq[key]) + ',' + str(sizeToWrite) + ','+ str(accessTime[key]) +'\n')
            cfList.append(key)
        '''

        f.write(key + ',' + str(req_time) + ',' + str(sizeToWrite[key]) + ','+ str(float(req_time) / sizeToWrite[key])  + '\n')

        time_size += float(req_time) / sizeToWrite[key]
        if count % policy_interval == 0:
            
            print "Getting bucket metrics...1"
            get_bucket_metrics()

            for k in accessFreq.keys():
                mi += sizeToWrite[k] / accessFreq[k]
                miDict[k] = sizeToWrite[k] / accessFreq[k]

            mi = mi/ policy_interval

            if count > 500:
                #move_from_cold_to_hot(accessTime)
                move_from_cold_to_hot_with_delta(accessTime)

            move_data(mi, miDict) ### HOT to COLD movement
            
            miDict = dict()
            accessFreq = dict()
            print "Getting bucket metrics...2"
            bucketMetrics.write(", ")
            get_bucket_metrics()

            bucketMetrics.write(", " + str(time_size))

            bucketMetrics.write("\n")
            delta_list[:] = []
            time_size = 0
            if count%10000 == 0:
                break
            

    for k in accessFreq.keys():
        print k
        cf.write(k + ',' + str(accessFreq[k]) + ',' + str(sizeToWrite[k]) + ','+ str(accessTime[k]) +'\n')


def main():
    print "Hello World!"
    random.seed(0)
    #populateMySql()
    #pl_simulator()
    aws_simulation()
    #plot_graph()
    #freq_count()
    cf.close()
    f.close()


if __name__ == '__main__':
    main()