import gensim
import six
input_file = "zhwiki-latest-pages-articles.xml.bz2"
wiki = gensim.corpora.WikiCorpus(input_file, lemmatize=False, dictionary={})
print("loading wiki")
output = open("ouput.txt",'w')
space = " "
i = 0
for text in wiki.get_texts():
    if six.PY3:
        output.write(b' '.join(text).decode('utf-8') + '\n')
    else:
        output.write(space.join(text) + "\n")
    i = i + 1
    if (i % 10000 == 0):
        print("Saved " + str(i) + " articles")
output.close()
print('finished')