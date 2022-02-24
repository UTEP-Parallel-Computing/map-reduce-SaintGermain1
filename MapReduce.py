#!/usr/bin/env python3
import time
import pymp
import re


def dictOfItems(docList=[]):
    #hate, love, death, night, sleep, time, henry, hamlet, you, my, blood, poison, macbeth, king, heart, honest

    with pymp.Parallel() as p:
        wordLock = p.lock #acquire a lock for parallel section
        nonSharedDict = {'hate': 0, 'love': 0, 'death': 0 , 'night': 0, 'sleep': 0 , 'time': 0,
                         'henry': 0 , 'hamlet': 0 , 'you': 0 , 'my': 0, 'blood': 0 , 'poison': 0,
                         'macbeth': 0 , 'king': 0 , 'heart': 0 , 'honest': 0}
        words = pymp.shared.dict(nonSharedDict)  #create shared dict
        for doc in p.iterate(docList):
            for word in words:
                length = len(re.findall(word, doc))
                wordLock.acquire()
                words[word] = length
                wordLock.release()

    print(words)

    return words

def main():
    """
    main function for when running as a script
    """
    i = 1
    docList = []
    while i < 9:
        with open('shakespeare'+str(i)+'.txt', encoding='UTF-8') as f:
            f.seek(0)
            string = f.read();
            docList.append(string)
            
            #wordList = re.compile('hate | love | death | night | sleep | time | henry | hamlet | you | my | blood |poison | macbeth | king | heart | honest', re.IGNORECASE)
            i = i+1
            f.close()
    #hate, love, death, night, sleep, time, henry, hamlet, you, my, blood, poison, macbeth, king, heart, honest
    #wordList = re.compile(['hate'] | ['love'] | ['death'] | ['night'] | ['sleep'] | ['time'] | ['henry'] | ['hamlet'] | ['you'] | ['my'] | ['blood'] | ['poison'] | ['macbeth'] | ['king'] | ['heart'] | ['honest'], re.IGNORECASE)

    list = dictOfItems(docList)


if __name__ == '__main__':
    # execute only if run as a script
    main()
