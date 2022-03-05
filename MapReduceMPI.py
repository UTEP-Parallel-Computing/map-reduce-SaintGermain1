"""
Name: Garrett Jones
For: CS 4175
Description: A parallel program that counts the instances of words across a set of documents
Instructions: Run in terminal: example line 'mpirun -n 4 python3 MapReduceMPI.py'
"""

import time
import pymp
import re
from mpi4py import MPI

# get the world communicator
comm = MPI.COMM_WORLD

# get our rank (process #)
rank = comm.Get_rank()

# get the size of the communicator in # processes
size = comm.Get_size()

# the global list
globalListOfDocs = ['shakespeare1.txt', 'shakespeare2.txt', 'shakespeare3.txt', 'shakespeare4.txt',
                    'shakespeare5.txt', 'shakespeare6.txt', 'shakespeare7.txt', 'shakespeare8.txt']
# the local list for this process
localList = []

wordCount = {'hate': 0, 'love': 0, 'death': 0, 'night': 0, 'sleep': 0, 'time': 0,
             'henry': 0, 'hamlet': 0, 'you': 0, 'my': 0, 'blood': 0, 'poison': 0,
             'macbeth': 0, 'king': 0, 'heart': 0, 'honest': 0}
docStrings = []
# thread 0 distributes the work
if rank is 0:
    print('Thread 0 distributing')
 
    docsPerThread = len(globalListOfDocs) / size

    # first setup thread 0s slice of the list
    localList = globalListOfDocs[:int( docsPerThread )]


    #compute thread 0's count:
    for doc in localList:
        with open(doc, encoding='UTF-8') as f:
            f.seek(0)
            string = f.read();
            docStrings.append(string.lower())
            f.close()
    for doc in docStrings:
        for word in wordCount:
            length = len(re.findall(word, doc))
            wordCount[word] = wordCount[word] + length
    print(f'Thread {rank} has {localList}')
    print(f'Thread {rank} has word count:\n{wordCount}')
    #send docs to other threads and receive word counts
    for process in range(1, size):
        #start and end of slice we're sending
        startOfSlice = int( docsPerThread * process )
        endOfSlice = int( docsPerThread * (process + 1) )

        sliceToSend = globalListOfDocs[startOfSlice:endOfSlice]
        comm.send(sliceToSend, dest=process, tag=0)

        #receive counts
        recvd_count = comm.recv(source=process, tag=1)
        print(f'Thread 0 received from {process}')
        for key in wordCount:
            if key in recvd_count:
                wordCount[key] = wordCount[key] + recvd_count[key]
    print(wordCount)

#everyone else receives docList and sends word counts
else:
    # receive doc slice from thread 0 with tag of 0
    localList = comm.recv(source=0, tag=0)
    print(f'Thread {rank} has {localList}')
    for doc in localList:
        with open(doc, encoding='UTF-8') as f:
            f.seek(0)
            string = f.read();
            docStrings.append(string.lower())
            f.close()
    for doc in docStrings:
        for word in wordCount:
            length = len(re.findall(word, doc))
            wordCount[word] = wordCount[word] + length
    print(f'Thread {rank} has word count: \n{wordCount}')
    comm.send(wordCount, dest=0, tag=1)

