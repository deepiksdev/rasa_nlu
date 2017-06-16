
# -*- coding: utf-8 -*-


import gensim
from gensim.models import Word2Vec
model = gensim.models.KeyedVectors.load_word2vec_format("wiki.zh.text.vector", binary=False)
s = model.most_similar(u'中文')
for i in s:
    print i[0] + str(i[1])
s = model.most_similar(u'吃饭')

for i in s:
    print i[0] + str(i[1])