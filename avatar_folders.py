#python 2.7

#with a list of PK1 values mapped to images, this script will build .zip packages of avatars for upload

import os
import csv
from shutil import copyfile, rmtree
import zipfile

# this assumes a "|" delimited file where the PK1 value (eg. _123_1) is the first column and the file identifier is the 2nd.
dataFile = 'list.csv'

# path to the image source
imageDir = ''

ext = ".jpg"

#this keeps the .zip packages at a reasonable size
batchsize = 100

#initiate the counters
count = 0
batch = 0

#the output package name
avatarsZip = zipfile.ZipFile("avatars.zip", "w", zipfile.ZIP_DEFLATED)

with open(dataFile) as csvFile:
    readCsv = csv.reader(csvFile, delimiter = "|")
    for row in readCsv:
        count = count + 1
        dirname = "user" + row[0]
        filename = row[1] + ext
        dst = dirname + "/" + filename
        print('Adding: ' + dst + ' to avatars_' + str(batch +1) + '.zip')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # just using sample.jpg as place holder for full path/filename
        # src = imageDir + '/' + row[1] + ext
        src = 'sample.jpg'
        copyfile(src, dst)
        avatarsZip.write(dirname, dst)
        rmtree(dirname)
        if count == batchsize:
          count = 0
          batch = batch + 1
          avatarsZip.close()
          os.rename("avatars.zip", "avatars_" + str(batch) + ".zip")
          avatarsZip = zipfile.ZipFile("avatars.zip", "w", zipfile.ZIP_DEFLATED)

# wrap up the last batch with less than the batchsize items
batch = batch + 1
avatarsZip.close()
os.rename("avatars.zip", "avatars_" + str(batch) + ".zip")