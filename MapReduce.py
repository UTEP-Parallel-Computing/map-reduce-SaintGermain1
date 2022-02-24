"""
Name: Garrett Jones
For: CS 4175
Description: A parallel program that counts the instances of words across a set of documents
Instructions: Run in terminal: example line 'OMP_NUM_THREADS=1 python3 MapReduce.py'
"""
#!/usr/bin/env python3
import time
import pymp
import re


def dictOfItems(docList=[]):
    #hate, love, death, night, sleep, time, henry, hamlet, you, my, blood, poison, macbeth, king, heart, honest
    nonSharedDict = {'hate': 0, 'love': 0, 'death': 0 , 'night': 0, 'sleep': 0 , 'time': 0,
                         'henry': 0 , 'hamlet': 0 , 'you': 0 , 'my': 0, 'blood': 0 , 'poison': 0,
                         'macbeth': 0 , 'king': 0 , 'heart': 0 , 'honest': 0}
    words = pymp.shared.dict(nonSharedDict)  #create shared dict
    start = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
    with pymp.Parallel() as p:
        wordLock = p.lock #acquire a lock for parallel section
        for doc in p.iterate(docList):
            for word in words:
                length = len(re.findall(word, doc))
                wordLock.acquire()
                words[word] += length
                wordLock.release()
    end = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
    elapsed = end - start
    print(f'\ntime to find words:\ntime_elapsed: {end - start: 0.4f} seconds')
    values = words.values()
    total_count = sum(values)
    return words, total_count

def main():
    """
    main function for when running as a script
    """
    start = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
    i = 1
    docList = []
    while i < 9:
        with open('shakespeare'+str(i)+'.txt', encoding='UTF-8') as f:
            f.seek(0)
            string = f.read();
            docList.append(string.lower())            
            i = i+1
            f.close()
    end = time.clock_gettime( time.CLOCK_MONOTONIC_RAW )
    elapsed = end - start
    print(f'\ntime for i/o:\ntime_elapsed: {end - start: 0.4f} seconds')
    
    list, total_count = dictOfItems(docList)
    print(list)
    print(f'\ntotal_count : %d' % total_count)
if __name__ == '__main__':
    # execute only if run as a script
    main()
