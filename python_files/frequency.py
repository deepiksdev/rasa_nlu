from __future__ import division
import re


f = open("cut_file.txt")
string = f.read()
strings = string.split("\n")

def parcours(list_of_article):
    vocab = set()
    frequency_vocab = dict()
    frequency_doc   = dict()
    i = 0
    for article in list_of_article:
        s = re.sub(' ','',article)
        ss = filter(None, s.split('/'))
        tmp = set()
        i = i + 1
        if i%100==0:
            print('reading \t'+str(i) +"\t document")
        for word in ss:
            tmp.add(word)
            if frequency_vocab.has_key(word):
                frequency_vocab[word]= frequency_vocab[word]+1
            else:
                frequency_vocab[word]=1
        for word in tmp:
            if frequency_doc.has_key(word):
                frequency_doc[word] = frequency_doc[word] + 1
            else:
                frequency_doc[word] = 1
            vocab.add(word)
    return frequency_doc,frequency_vocab,vocab
frequency_doc,frequency_vocab,vocab = parcours(strings)
l = len(vocab)
print("finish reading")
f_write = open("frequency.txt",'w')
k = 0.0
point = 1
for i in vocab:
    k = k + 1
    f_write.write(str(frequency_vocab) + "\t" + str(frequency_doc) + "\t" + i + "\n" )
    pro = k/l
    if pro>point:
        print("finish " + str(pro) + "writing")
        point = point + 1
print "finished"



