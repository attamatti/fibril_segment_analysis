#!/usr/bin/python
##############################################
### FETCH COPY - (fbsmi2018-06-19 08:25:18.824032) - download a fresh copy if necessary
##############################################

##############################################
### FETCH COPY - (fbsmi2017-02-06 09:01:07.882601) - download a fresh copy if necessary
##############################################

# generalized script for messing with starfiles


import sys

#------- function test if string is a number --------------------------#
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#-----------------------------------------------------------------------

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

#------ function: write all of the numbers in the fortran format ---------------------------#
def make_pretty_numbers(dataarray):
    prettyarray = []
    for line in dataarray:
        linestr = ""
        for i in line:
            if is_number(i):
                count = len(i.split('.'))
                if count > 1:
                    i = float(i)
                    if len(str(i).split('.')[0]) > 5:
                        linestr= linestr+"{0:.6e} ".format(i)
                    else:
                        linestr= linestr+"{0:12.6f} ".format(i)
                else:
                    linestr= linestr+"{0: 12d} ".format(int(i))
            else:
                linestr= linestr+"{0} ".format(i)
        prettyarray.append(linestr)
    return prettyarray
#---------------------------------------------------------------------------------------------#



(mic_labels,mic_header,mic_data) = read_starfile(sys.argv[1])
fib_data = open(sys.argv[2],'r').readlines()

ctfdic = {}
for i in mic_data:
    ctfdic[i[mic_labels['_rlnMicrographName ']].split('/')[-1].split('.')[0]] = i[1:]

output = open('fibrils_ctf.star','w')
for i in mic_header:
    output.write('{0}\n'.format(i))

newdata = []
for i in fib_data:
    id = i.split('/')[-1].split('_fil')[0].strip('\n')
    if id in ctfdic:
        output.write('{0}  '.format(i.strip('\n')))
        for j in ctfdic[id]:
            output.write('{0}  '.format(j))
        output.write('\n')

