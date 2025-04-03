#!/usr/bin/python3
# -*- coding: utf-8 -*-

from extract.graphcollection import GraphCollection

import random

import cgi
import cgitb
import json
import os
import sys


#cgitb.enable()

class Main:
    gc = None

    qd1g_f  = None
    qd2g_f  = None
    qd3g_f  = None
    length_f = None
    
    qd1g_h   = None
    qd2g_h   = None
    qd3g_h   = None
    length_h = None

    def run(self):
        def avg(listObj):
            return float(sum(listObj)) / len(listObj)
        
        def median(listObj):
            sorts = sorted(listObj)
            length = len(sorts)
            midIdx = int(length/2)
            if not length % 2:
                return (sorts[midIdx] + sorts[midIdx - 1]) / 2
            return sorts[midIdx]

        def mode(listObj):
            from collections import Counter
            data = Counter(listObj)
            return data.most_common(1)

        def timeIt(f, *args):
            import time
            start = time.clock()
            m = f(*args)
            return m, (time.clock() - start)*10
        
        def findWords(count, Qdict = self.qd3g_f, depth = 3, lengthObj = self.length_f):
            words = []
            for i in range(count):
                if type(lengthObj) == tuple:
                    length = self.gc.findLength(lengthObj)
                else:
                    length = lengthObj
                word = self.gc.findWord(Qdict, depth, length)
                words.append(word)
            return words

        def compareMethods(afile, oc, qd3g, qd2g, prob):
            probTotal1 = []
            probTotal2 = []
            probTotal3 = []
            print("Mõõdiku võrdlus:")
            for i in range(10000):
                word1 = self.random_line(afile) #originaal
                wordlen = len(word1)
                word2 = oc.findWord(qd2g, 2, wordlen) #digraaf
                word3 = oc.findWord(qd3g, 3, wordlen) #trigraaf
                prob1 = oc.findWordProbability(word1,prob,1) #* 10**6
                prob2 = oc.findWordProbability(word2,prob,1) #* 10**6
                prob3 = oc.findWordProbability(word3,prob,1) #* 10**6
                probTotal1.append(prob1)
                probTotal2.append(prob2)
                probTotal3.append(prob3)
                #print ("Sõna1: %s Tõenäosus: %.3g" % (word1, prob1))
                #print ("Sõna2: %s Tõenäosus: %.3g" % (word2, prob2))
                #print ("Sõna3: %s Tõenäosus: %.3g" % (word3, prob3))
            print('ORIGINAAL min, avg, median, max tõenäosus 1: %.3g, %.3g, %.3g, %.3g' % (min(probTotal1),avg(probTotal1), median(probTotal1),max(probTotal1)))
            print('DIGRAMM min, avg, , median, max tõenäosus 2: %.3g, %.3g, %.3g, %.3g' % (min(probTotal2),avg(probTotal2), median(probTotal2), max(probTotal2)))
            print('TRIGRAMM min, avg, , median, max tõenäosus 3: %.3g, %.3g, %.3g, %.3g' % (min(probTotal3),avg(probTotal3), median(probTotal3), max(probTotal3)))

        def lengthTest(gc,length):
            lengths = []
            for i in range(100000):
                lengths.append(gc.findLength(length))
            return min(lengths), avg(lengths), median(lengths), max(lengths)

        def findMetric(words, gc, probQD):
            for word in words:
                print ('Sõna: %s tõenäosus on: %.3g' % (word, gc.findWordProbability(word,probQD,1)))

                
        def cgiOutput():
            def chooseAndGet():
                form = cgi.FieldStorage()
                result = {}
                len = None
                if 'len' in form:
                    try:
                        if int(form['len'].value) < 50 and int(form['len'].value) > 2:
                            len = int(form['len'].value)
                    except ValueError:
                        pass
                if 'how' in form:
                    if   form['how'].value == 'dgf':
                        if not len:
                            len = self.length_f
                        result = findWords(20, self.qd2g_f, 2, len)
                    elif form['how'].value == 'tgf':
                        if not len:
                            len = self.length_f
                        result = findWords(20, self.qd3g_f, 3, len)
                    elif form['how'].value == 'dgh':
                        if not len:
                            len = self.length_h
                        result = findWords(20, self.qd2g_h, 2, len)
                    elif form['how'].value == 'tgh':
                        if not len:
                            len = self.length_h
                        result = findWords(20, self.qd3g_h, 3, len)
                return json.dumps(result)

            print ("Content-type:text/html;encoding=UTF-8")
            print ()
            if ('REQUEST_METHOD' in os.environ and
                os.environ['REQUEST_METHOD'] == 'POST'):
                print(chooseAndGet())

        def shellOutput():
            #print(lengthTest(self.gc, self.length_f))
            
            #words = ('htamasvu', 'seekalti', 'hapäraus', 'lilestis', 'tisilmma')
            words = ('eektrond', 'kuvkarkp', 'isatopun', 'apakseli', 'mergurmi',
                     'aksindik', 'kipeenam', 'põhjuhem', 'sidussaa', 'annstann')
            words = ('kaigenda', 'päikulte', 'liidusam', 'metastap', 'väivolis',
                     'väivolis', 'palbapre', 'soongiaa', 'ereelatu', 'nargaste', 'tsülduku')
            #words =  ('tiiminst', 'almilinn', 'rotselva', 'vahulinv', 'noomumbi')
            #words = ('haigeduv', 'sistamat', 'igatsivi', 'särklaag', 'andrilin')
            #words = ('htamasvu','õhesteni', 'oorusaja', 'tiuspial', 'avõhuria', 'tasimisu')
            #findMetric(words, self.gc, self.qd1g_f)
            '''
            a = compareMethods('resource/lemmad_utf.txt',
                           self.gc, self.qd3g_h,
                           self.qd2g_h, self.qd1g_h)
            '''
            '''
            lst = []
            with open('resource/lemmad_utf.txt', 'r') as f:
                for l in f.readlines():
                    lst.append(len(l))
            print ('Min: %s, Avg: %s Keskv: %s Max: %s' % (min(lst), avg(lst), median(lst),max(lst)))
            '''
        if 'GATEWAY_INTERFACE' in os.environ:
            cgiOutput()
        else:
            shellOutput()
        return

    def save(self):

        def scanAndSave():
            qd = GraphCollection()
            fileName1 = 'resource/lemmad_utf.txt'
            fileName2 = 'resource/lemmad_piir_utf.txt'
            trie1 = qd.createTrie(fileName1, 3)
            trie2 = qd.createTrie(fileName2, 3)
            length1       = qd.createLengthQuickArr(fileName1)
            length2       = qd.createLengthQuickArr(fileName2)
            probability1  = qd.createQuickDict(trie1, 1)
            probability2  = qd.createQuickDict(trie2, 1)
            generatorD1    = qd.createQuickDict(trie1, 2)
            generatorD2    = qd.createQuickDict(trie2, 2)
            generatorT1    = qd.createQuickDict(trie1, 3)
            generatorT2    = qd.createQuickDict(trie2, 3)

            qd.save('resource/qd3g_f.pck', generatorT1)
            qd.save('resource/qd2g_f.pck', generatorD1)
            qd.save('resource/qd1g_f.pck', probability1)
            qd.save('resource/lngt_f.pck', length1)
            
            qd.save('resource/qd3g_h.pck', generatorT2)
            qd.save('resource/qd2g_h.pck', generatorD2)
            qd.save('resource/qd1g_h.pck', probability2)
            qd.save('resource/lngt_h.pck', length2)

        scanAndSave()


    def load(self):

        def loadOptimized(self):
            self.gc = GraphCollection()
            self.qd1g_f = self.gc.load('resource/qd1g_f.pck')
            self.qd2g_f = self.gc.load('resource/qd2g_f.pck')
            self.qd3g_f = self.gc.load('resource/qd3g_f.pck')
            self.length_f = self.gc.load('resource/lngt_f.pck')
            
            self.qd1g_h = self.gc.load('resource/qd1g_h.pck')
            self.qd2g_h = self.gc.load('resource/qd2g_h.pck')
            self.qd3g_h = self.gc.load('resource/qd3g_h.pck')
            self.length_h = self.gc.load('resource/lngt_h.pck')

        loadOptimized(self)

    def random_line(self,afile):
        return random.choice(list(open(afile))).rstrip('\n')


    # TODO: implement new where only needed pickle is loaded and solutions given.
def getWords(self, how, length):
    # sanitize
    if how not in ["dgf", "tgf", "dgh", "tgh"]:
        return {}
    if int(len) > 49 or int(len) < 2:
        return {}

    for i in range(count):
        length = self.gc.findLength(lengthObj)
        word = self.gc.findWord(Qdict, depth, length)
        words.append(word)
    return words

    if 'how' in form:
        if how == 'dgf':
            filename = 'resource/qd2g_f.pck'
            depth = 2
            result = findWords(20, self.qd2g_f, 2, len)
        elif form['how'].value == 'tgf':
            result = findWords(20, self.qd3g_f, 3, len)
        elif form['how'].value == 'dgh':
            result = findWords(20, self.qd2g_h, 2, len)
        elif form['how'].value == 'tgh':
            result = findWords(20, self.qd3g_h, 3, len)

    collection = {}
    with open(filename, 'rb') as f:
        collection = pickle.load(f)
    result = findWords(20, collection, depth, length)
    return json.dumps(result)
